from flask import Response, request, Blueprint
import requests, json

from pymp_common.flask.routes.media import index, get_media
from pymp_common.flask.routes.ffmpeg import ffmpeg_meta, ffmpeg_thumb

from ...app.PympConfig import pymp_env
from ...dataaccess.redis import media_path_da, media_meta_da, media_thumb_da
from ...dataaccess.http_request_factory import media_request_factory, ffmpeg_request_factory
from ...utils.Request import get_request_range

app_frontend_media = Blueprint('app_frontend_media',__name__)
app_frontend_meta = Blueprint('app_frontend_meta',__name__)
app_frontend_thumb = Blueprint('app_frontend_thumb', __name__)

@app_frontend_media.route('/api/media/<string:id>')
def media(id):
    reqByte1, reqByte2 = get_request_range(request)
    
    if(pymp_env.media_api_base_url() == pymp_env.media_svc_base_url()):
        return get_media(id)   
    else:   
        apiRequest = media_request_factory.get_media(id, reqByte1, request)        
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
    if not media_path_da.has():      
        if(pymp_env.media_api_base_url() == pymp_env.media_svc_base_url()):
            index()
        else: 
            apiRequest = media_request_factory.get_media_index()     
            s = requests.Session()
            s.send(apiRequest.prepare())    
        
    media_paths = media_path_da.hgetall()
    ids=[]
    if media_paths:
        for id in media_paths.keys():
            ids.append(id)
        
    return Response(json.dumps(ids), mimetype='application/json')

@app_frontend_meta.route('/api/meta/<string:id>')
def meta(id):     
    if not media_meta_da.has(id):
        if(pymp_env.media_api_base_url() == pymp_env.ffmpeg_svc_base_url()):
            ffmpeg_meta(id)  
        else:
            apiRequest = ffmpeg_request_factory.get_meta(id)    
            s = requests.Session()
            s.send(apiRequest.prepare())
        
    media_meta = media_meta_da.get(id)
    return Response(media_meta)


@app_frontend_thumb.route('/api/thumb/<string:id>')
def thumb(id):
    if not media_thumb_da.has(id):
        if(pymp_env.media_api_base_url() == pymp_env.ffmpeg_svc_base_url()):
            ffmpeg_thumb(id)  
        else:
            apiRequest = ffmpeg_request_factory.get_thumb(id)
            s = requests.Session()
            s.send(apiRequest.prepare())

    media_thumb = media_thumb_da.get(id)
    return Response(media_thumb, content_type="image/png")

@app_frontend_meta.after_request
@app_frontend_media.after_request
@app_frontend_thumb.after_request
def after_request(response):
    response.headers.set('Accept-Ranges', 'bytes')
    response.headers.set('Access-Control-Allow-Origin', pymp_env.get("CORS_HEADER"))
    return response