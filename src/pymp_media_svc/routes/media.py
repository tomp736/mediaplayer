from flask import Response, request, Blueprint
import json
import bz2

from ..services.MediaFileService import MediaFileService
from pymp_common.services.HttpServices import ThumbService, MetaService
from pymp_common.services.RedisServices import MediaPathService
from pymp_common.utils.Request import get_request_range

app_media = Blueprint('app_media',__name__)

@app_media.route('/media/<string:id>')
def media(id):
    reqByte1, reqByte2 = get_request_range(request)
    
    # request path from redis
    media_path_c = MediaPathService.get_redis()
    media_path = ""
    if MediaPathService.has_media_path_index(media_path_c):
        media_path_index = MediaPathService.get_media_path_index(media_path_c)
        media_path = media_path_index.get(id) or ""
        if media_path == "":
            response = Response(status=404)
            return response
    
    # read chunk
    chunk, start, length, file_size = MediaFileService.get_media_chunk(media_path ,id, reqByte1, reqByte2)
        
    # write response
    response = Response(chunk, 206, mimetype='video/webm', content_type='video/webm')
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    # response.headers.add('Transfer-Encoding', 'chunked')
    return response

@app_media.route('/media/list')
def list():
    media_path_index, media_size_index = MediaFileService.get_media_indexes()    
    keys = []
    for key in media_path_index.keys():
        keys.append(key)
    
    return Response(json.dumps(keys), mimetype='application/json')

@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response