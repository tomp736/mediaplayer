from flask import Response, request, Blueprint
import requests, json

from pymp_common.app.PympConfig import PympServer
from pymp_common.flask.routes.media import get_media
from pymp_common.flask.routes.ffmpeg import ffmpeg_meta, ffmpeg_thumb

from ...app.PympConfig import pymp_env
from ...dataaccess.redis import media_source_da, media_service_da, media_meta_da, media_thumb_da
from ...dataaccess.http_request_factory import media_request_factory
from ...utils.Request import get_request_range

app_frontend_media = Blueprint('app_frontend_media',__name__)
app_frontend_meta = Blueprint('app_frontend_meta',__name__)
app_frontend_thumb = Blueprint('app_frontend_thumb', __name__)

@app_frontend_media.route('/api/media/<string:id>')
def media(id):    
    # if api is also media_svc
    if(pymp_env.getServerType() & PympServer.MEDIA_SVC):
        return get_media(id)  
    
    # default to pymp_env media_svc
    media_svc_url = None
    
    # check if media_source exists in redis
    if media_source_da.has():
        # get sourceid by mediaid
        sourceid = media_source_da.hget(id)
        
        if sourceid and media_service_da.has():
            # get service info by sourceid
            serviceinfo = media_service_da.hget(sourceid)
            if serviceinfo:
                media_svc_scheme = serviceinfo["scheme"]
                media_svc_host = serviceinfo["host"]
                media_svc_port = serviceinfo["port"]
                media_svc_url = f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"            

    if media_svc_url is None:
        return Response(status=404)
    
    reqByte1, reqByte2 = get_request_range(request)    
    apiRequest = media_request_factory._get_media_(media_svc_url, id, reqByte1, request)        
    s = requests.Session()
    apiResponse = s.send(apiRequest.prepare())
    response = Response(apiResponse.content)
    
    response.status_code = apiResponse.status_code
    if not apiResponse.headers.get("Content-Range") is None:
        response.headers.set('Content-Range', apiResponse.headers['Content-Range'])
    if not apiResponse.headers.get("Content-Type") is None:
        response.headers.set('Content-Type', apiResponse.headers['Content-Type'])
        
    return response

@app_frontend_media.route('/api/media/list')
def list(): 
    media_sources = media_source_da.hgetall()
    media_ids = []
    if not media_sources is None:
        for mediaid in media_sources.keys():            
            media_ids.append(mediaid)
    return Response(json.dumps(media_ids), status=200, content_type="application/json")


@app_frontend_meta.route('/api/meta/<string:id>')
def meta(id):     
    if not media_meta_da.has(id):
        if(pymp_env.getServerType() & PympServer.FFMPEG_SVC):
            ffmpeg_meta(id)  
        else:
            return Response(status=404)
        
    media_meta = media_meta_da.get(id)
    return Response(media_meta)


@app_frontend_thumb.route('/api/thumb/<string:id>')
def thumb(id):
    if not media_thumb_da.has(id):
        if(pymp_env.getServerType() & PympServer.FFMPEG_SVC):
            ffmpeg_thumb(id)  
        else:
            return Response(status=404)

    media_thumb = media_thumb_da.get(id)
    return Response(media_thumb, content_type="image/png")

@app_frontend_meta.after_request
@app_frontend_media.after_request
@app_frontend_thumb.after_request
def after_request(response):
    response.headers.set('Accept-Ranges', 'bytes')
    response.headers.set('Access-Control-Allow-Origin', pymp_env.get("CORS_HEADER"))
    return response