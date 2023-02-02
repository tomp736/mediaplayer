import logging
from flask import Blueprint
from flask import Response
from flask import request
from flask import redirect
import json
from pymp_common.abstractions.providers import MediaChunk
from pymp_common.app import ProviderFactory
from pymp_common.app.Services import mediaRegistryService

from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.redis import media_meta_da
from pymp_common.dataaccess.redis import media_thumb_da
from pymp_common.services.MediaService import MediaService

app_frontend_media = Blueprint('app_frontend_media', __name__)
app_frontend_meta = Blueprint('app_frontend_meta', __name__)
app_frontend_thumb = Blueprint('app_frontend_thumb', __name__)


@app_frontend_media.route('/api/media/<string:media_id>')
def media(media_id):
    reqByte1, reqByte2, fileSize = MediaChunk.parse_range_header(
        request.headers["range"])
    service_id = mediaRegistryService.get_media_service(media_id)
    mediaService = MediaService(
        mediaRegistryService.MediaRegistryDataProvider,
        ProviderFactory.get_media_provider(service_id))

    mediaChunk = mediaService.get_media_chunk(media_id, reqByte1, reqByte2)
    if mediaChunk:
        response = Response(
            mediaChunk.chunk,
            206,
            mimetype='video/webm',
            content_type='video/webm')

        response.headers.set(
            'Content-Range', mediaChunk.to_content_range_header()
        )
        return response
    return Response(status=400)


@app_frontend_media.route('/api/media/list')
def list():
    mediaIndex = mediaRegistryService.get_media_index()
    logging.info(mediaIndex)
    mediaIds = []
    if mediaIndex:
        for media_id in mediaIndex:
            mediaIds.append(media_id)
    return Response(json.dumps(mediaIds), status=200, content_type="application/json")


@app_frontend_meta.route('/api/meta/<string:media_id>')
def meta(media_id):
    media_meta = media_meta_da.get(media_id)
    if media_meta:
        return Response(media_meta)
    return {}


@app_frontend_thumb.route('/api/thumb/<string:media_id>')
def thumb(media_id):
    media_thumb = media_thumb_da.get(media_id)
    return Response(media_thumb, content_type="image/png")


@app_frontend_meta.after_request
@app_frontend_media.after_request
@app_frontend_thumb.after_request
def after_request(response):
    response.headers.set('Accept-Ranges', 'bytes')
    response.headers.set('Access-Control-Allow-Origin',
                         pymp_env.get("CORS_HEADER"))
    return response
