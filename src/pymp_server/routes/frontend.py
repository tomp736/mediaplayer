import logging
import json

from flask import Blueprint
from flask import Response
from flask import request
from flask import redirect
from pymp_core.abstractions.providers import MediaChunk

from pymp_core.app.PympConfig import pymp_env
from pymp_core.app.Services import media_service
from pymp_core.app.Services import media_registry_service

app_frontend_media = Blueprint('app_frontend_media', __name__)
app_frontend_meta = Blueprint('app_frontend_meta', __name__)
app_frontend_thumb = Blueprint('app_frontend_thumb', __name__)


@app_frontend_media.route('/api/media/<string:media_id>')
def get_media_chunk(media_id):
    start_byte, end_byte, file_size = MediaChunk.parse_range_header(
        request.headers["range"])
    mediaChunk = media_service.get_media_chunk(media_id, start_byte, end_byte)
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
    media_index_keys = list(media_registry_service.get_media_registry_provider().get_all_media_info().keys())
    return Response(json.dumps(media_index_keys), status=200, content_type="application/json")


@app_frontend_meta.route('/api/meta/<string:media_id>')
def get_media_meta(media_id):
    media_meta = media_service.get_media_meta(media_id)
    if media_meta:
        return Response(media_meta)
    return {}


@app_frontend_thumb.route('/api/thumb/<string:media_id>')
def get_media_thumb(media_id):
    media_thumb = media_service.get_media_thumb(media_id)
    return Response(media_thumb, content_type="image/png")


@app_frontend_meta.after_request
@app_frontend_media.after_request
@app_frontend_thumb.after_request
def after_request(response):
    response.headers.set('Accept-Ranges', 'bytes')
    response.headers.set('Access-Control-Allow-Origin',
                         pymp_env.get("CORS_HEADER"))
    return response
