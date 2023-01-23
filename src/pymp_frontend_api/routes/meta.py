from flask import Response, Blueprint
import requests
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.redis import media_meta_da
from pymp_common.dataaccess.http_request_factory import ffmpeg_request_factory

app_meta = Blueprint('app_meta',__name__)

@app_meta.route('/meta/<string:id>')
def meta(id): 
    if not media_meta_da.has(id):
        apiRequest = ffmpeg_request_factory.get_meta(id)    
        s = requests.Session()
        s.send(apiRequest.prepare())
        
    media_meta = media_meta_da.get(id)
    return Response(media_meta)

@app_meta.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Access-Control-Allow-Origin', pymp_env.get("FEAPI_CORS_HEADER"))
    return response
