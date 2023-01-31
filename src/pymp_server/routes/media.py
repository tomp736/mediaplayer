import json
import logging
from flask import Response
from flask import request
from flask import Blueprint

from pymp_common.abstractions.providers import MediaChunk
from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.Services import mediaService

app_media = Blueprint('app_media', __name__)

@app_media.route('/media/<string:mediaId>', methods=['GET'])
def get_media(mediaId):
    reqByte1, reqByte2, fileSize = MediaChunk.parse_range_header(request.headers["Range"])    
    mediaChunk = mediaService.get_media_chunk(pymp_env.get("SERVER_ID"), mediaId, reqByte1, reqByte2)
    if mediaChunk:
        response = Response(
            mediaChunk.chunk, 
            206, 
            mimetype='video/webm', 
            content_type='video/webm')
        
        response.headers.set(
            'Content-Range', mediaChunk.to_content_range_header()
            )
        logging.info(response)
        logging.info(response.headers)
        return response
        
    return Response(status=400)

@app_media.route('/media', methods=['POST'])
def post_media():
    if request.method == 'POST':
        if not mediaService:
            return Response(status=400)
        mediaService.save_media(pymp_env.get("SERVER_ID"),"output_file", request.stream)
    return Response(status=404)

@app_media.route('/media/index', methods=['GET'])
def index():
    if not mediaService:
        return Response(status=400)
    mediaService.update_index(pymp_env.get("SERVER_ID"))
    return Response(status=200)

@app_media.route('/media/list', methods=['GET'])
def list(): 
    if not mediaService:
        return Response(status=400) 
    mediaIds = mediaService.get_media_ids(pymp_env.get("SERVER_ID"))       
    return Response(json.dumps(mediaIds), mimetype='application/json')

@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
