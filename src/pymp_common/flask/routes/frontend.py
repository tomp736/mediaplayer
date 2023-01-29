from flask import Response, request, Blueprint
import json
from pymp_common.abstractions.providers import MediaChunk
from pymp_common.app.Services import mediaRegistryService, mediaService

from ...app.PympConfig import pymp_env
from ...dataaccess.redis import  media_meta_da, media_thumb_da

app_frontend_media = Blueprint('app_frontend_media',__name__)
app_frontend_meta = Blueprint('app_frontend_meta',__name__)
app_frontend_thumb = Blueprint('app_frontend_thumb', __name__)

@app_frontend_media.route('/api/media/<string:mediaId>')
def media(mediaId): 
    reqByte1, reqByte2, fileSize = MediaChunk.parse_range_header(request.headers["range"])        
    mediaChunk = mediaService.get_media_chunk(mediaId, reqByte1, reqByte2)   
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

@app_frontend_media.route('/api/media/list')
def list(): 
    mediaIndex = mediaRegistryService.getMediaIndex()
    mediaIds = []
    if mediaIndex:
        for mediaId in mediaIndex:
            mediaIds.append(mediaId)
    return Response(json.dumps(mediaIds), status=200, content_type="application/json")


@app_frontend_meta.route('/api/meta/<string:mediaId>')
def meta(mediaId):        
    media_meta = media_meta_da.get(mediaId)
    return Response(media_meta)


@app_frontend_thumb.route('/api/thumb/<string:mediaId>')
def thumb(mediaId):
    media_thumb = media_thumb_da.get(mediaId)
    return Response(media_thumb, content_type="image/png")

@app_frontend_meta.after_request
@app_frontend_media.after_request
@app_frontend_thumb.after_request
def after_request(response):
    response.headers.set('Accept-Ranges', 'bytes')
    response.headers.set('Access-Control-Allow-Origin', pymp_env.get("CORS_HEADER"))
    return response