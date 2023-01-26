import json
import logging
import os
from flask import Response, request, Blueprint

from ...app.MediaDirectoryService import media_directory_service
from ...utils.Request import get_request_range

app_media = Blueprint('app_media', __name__)


@app_media.route('/media/<string:id>', methods=['GET'])
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

@app_media.route('/media', methods=['POST'])
def post_media():
    if request.method == 'POST':
        filefolder = media_directory_service.mediapath
        fullpath = os.path.join(filefolder, "output_file") 
        
        with open(fullpath, "bw") as f:
            chunk_size = 4096
            while True:
                chunk = request.stream.read(chunk_size)
                if len(chunk) == 0:
                    media_directory_service.update_index() 
                    return Response(status=200)
                f.write(chunk)
        
    return Response(status=404)

@app_media.route('/media/index', methods=['GET'])
def index():
    media_directory_service.update_index()
    return Response(status=200)

@app_media.route('/media/list', methods=['GET'])
def list(): 
    ids=[]
    for id in media_directory_service.index.keys():
        ids.append(id)
    return Response(json.dumps(ids), mimetype='application/json')

@app_media.route('/media/dictionary', methods=['GET'])
def dictionary(): 
    return Response(json.dumps(media_directory_service.index), mimetype='application/json')

@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
