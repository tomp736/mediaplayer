from flask import Response, request, Blueprint
import requests, json
from pymp_common.services.HttpServices import FeApiService
from pymp_common.services.ConfigService import ConfigService
from pymp_common.utils.Request import get_request_range

app_media = Blueprint('app_media',__name__)

@app_media.route('/media/<string:id>')
def video(id):
    reqByte1, reqByte2 = get_request_range(request)
    mediaUrl=FeApiService.get_media_url(id)    
    mediaHeaders = {
        'Range': f'bytes {reqByte1}-{reqByte2}'
    }
    
    mediaResponse = requests.get(mediaUrl, headers=mediaHeaders)
    
    response = Response(mediaResponse.content, 206, mimetype='video/webm', content_type='video/webm')
    response.headers.add('Content-Range', mediaResponse.headers['Content-Range'])
    # response.headers.add('Transfer-Encoding', 'chunked')
    return response

@app_media.route('/media/list')
def list():
    media_list=FeApiService.get_media_list()
    return Response(json.dumps(media_list), mimetype='application/json')

@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

