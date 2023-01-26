import json
import logging
from flask import Response, request, Blueprint

from ...app.MediaDirectoryService import media_directory_service
from ...utils.Request import get_request_range

app_media = Blueprint('app_media', __name__)


@app_media.route('/media/<string:id>')
def get_media(id):
    reqByte1, reqByte2 = get_request_range(request)

    logging.info(media_directory_service.index)
    
    media_path = media_directory_service.index.get(id)
    if media_path:        
        chunk, start, length, file_size = media_directory_service.get_media_chunk(
            id, 
            reqByte1, 
            reqByte2)
        
        response = Response(
            chunk, 
            206, 
            mimetype='video/webm', 
            content_type='video/webm')
        
        response.headers.set(
            'Content-Range', 
            'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
        
        return response
    return Response(status=404)

@app_media.route('/media/index')
def index():
    media_directory_service.update_index()
    return Response(status=200)

@app_media.route('/media/list')
def list(): 
    ids=[]
    for id in media_directory_service.index.keys():
        ids.append(id)
    return Response(json.dumps(ids), mimetype='application/json')

@app_media.route('/media/dictionary')
def dictionary(): 
    return Response(json.dumps(media_directory_service.index), mimetype='application/json')

@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
