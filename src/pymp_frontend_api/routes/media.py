from flask import Response, request, Blueprint
import requests, json
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.redis import media_path_da
from pymp_common.dataaccess.http_request_factory import media_request_factory
from pymp_common.utils.Request import get_request_range

app_media = Blueprint('app_media',__name__)

@app_media.route('/media/<string:id>')
def media(id):
    reqByte1, reqByte2 = get_request_range(request)
    
    apiRequest = media_request_factory.get_media(id, reqByte1, request)        
    s = requests.Session()
    apiResponse = s.send(apiRequest.prepare())
        
    response = Response(apiResponse.content)
    
    response.status = apiResponse.status_code        
    if not apiResponse.headers.get("Content-Range") is None:
        response.headers.set('Content-Range', apiResponse.headers['Content-Range'])
    if not apiResponse.headers.get("Content-Type") is None:
        response.headers.set('Content-Type', apiResponse.headers['Content-Type'])
        
    return response

@app_media.route('/media/list')
def list():        
    if not media_path_da.has():        
        apiRequest = media_request_factory.get_media_index()     
        s = requests.Session()
        s.send(apiRequest.prepare())
        
    media_paths = media_path_da.hgetall()
    ids=[]
    if media_paths:
        for id in media_paths.keys():
            ids.append(id)
        
    return Response(json.dumps(ids), mimetype='application/json')

@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Access-Control-Allow-Origin', pymp_env.get("FEAPI_CORS_HEADER"))
    return response

