import json
import logging
import os
from flask import Response, request, Blueprint

from pymp_common.providers.MediaProviderFactory import MediaServiceFactory
from ...utils.Request import get_request_range

app_media = Blueprint('app_media', __name__)

mediaProvider = MediaServiceFactory.create_instance()

@app_media.route('/media/<string:id>', methods=['GET'])
def get_media(id):
    reqByte1, reqByte2 = get_request_range(request)  
    mediaChunk = mediaProvider.get_media_chunk(id, reqByte1, reqByte2)

    if mediaChunk:
        response = Response(
            mediaChunk.chunk, 
            206, 
            mimetype='video/webm', 
            content_type='video/webm')
        
        response.headers.set(
            'Content-Range', mediaChunk.toContentRangeHeader()
            )
        return response
        
    return Response(status=400)

@app_media.route('/media', methods=['POST'])
def post_media():
    if request.method == 'POST':
        mediauri = mediaProvider.get_media_uri("output_file")
        mediaProvider.postMedia(request.stream)        
        
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
