import logging
import json

from flask import Blueprint
from flask import Response
from flask import request
from flask import redirect
from pymp_core.abstractions.providers import MediaChunk
from pymp_core.app.config_factory import CONFIG_FACTORY

from pymp_core.app.services import MEDIA_SERVICE
from pymp_core.app.services import MEDIA_REGISTRY_SERVICE

app_frontend_media = Blueprint('app_frontend_media', __name__)

@app_frontend_media.route('/api/media/<string:media_id>')
def get_media_chunk(media_id):
    start_byte, end_byte, file_size = MediaChunk.parse_range_header(
        request.headers["range"])
    mediaChunk = MEDIA_SERVICE.get_media_chunk(media_id, start_byte, end_byte)
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
def get_media_list():
    media_index_keys = list(MEDIA_REGISTRY_SERVICE.get_media_registry_provider().get_all_media_info().keys())
    return Response(json.dumps(media_index_keys), status=200, content_type="application/json")