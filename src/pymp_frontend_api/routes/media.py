from flask import Response, request, Blueprint
import requests, json
from pymp_common.services.HttpServices import MediaService
from pymp_common.services.RedisServices import MediaPathService
from pymp_common.services.ConfigService import ConfigService
from pymp_common.utils.Request import get_request_range

app_video = Blueprint('app_video',__name__)

@app_video.route('/media/<string:id>')
def video(id):
    reqByte1, reqByte2 = get_request_range(request)
    mediaUrl=MediaService.get_media_url(id)    
    mediaHeaders = {
        'Range': f'bytes {reqByte1}-{reqByte2}'
    }    
    mediaResponse = requests.get(mediaUrl, headers=mediaHeaders)
    
    response = Response(mediaResponse.content, 206, mimetype='video/webm', content_type='video/webm')
    response.headers.add('Content-Range', mediaResponse.headers['Content-Range'])
    # response.headers.add('Transfer-Encoding', 'chunked')
    return response

@app_video.route('/media/list')
def list():
    media_path_c=MediaPathService.get_redis()
    if MediaPathService.has_media_path_index(media_path_c):
        MediaService.get_media_index()
        
    media_path_index=MediaPathService.get_media_path_index(media_path_c) 
    
    ids=[]
    for id in media_path_index.keys():
        ids.append(id)
        
    return Response(json.dumps(ids), mimetype='application/json')

@app_video.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

