import os
from flask import Response, request, Blueprint
import requests

from pymp_common.dataaccess.redis import media_da, media_length_da, media_path_da
from pymp_common.dataaccess.http_request_factory import ffmpeg_request_factory
from ..services.MediaFileService import MediaFileService
from pymp_common.utils.Request import get_request_range

app_media = Blueprint('app_media', __name__)


@app_media.route('/media/<string:id>')
def media(id):
    reqByte1, reqByte2 = get_request_range(request)

    # filesystem
    if media_path_da.has() and media_path_da.hhas(id):
        media_path = media_path_da.hget(id)
        if media_path:
            if not os.path.isfile(media_path):
                media_path_da.hdel(id)
                media_length_da.hdel(id)
            else:
                chunk, start, length, file_size = MediaFileService.get_media_chunk(
                    media_path, reqByte1, reqByte2)
                response = Response(
                    chunk, 206, mimetype='video/webm', content_type='video/webm')
                response.headers.set(
                    'Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
                return response

    # catch all
    if not media_da.has("static"):
        apiRequest = ffmpeg_request_factory.get_static()
        s = requests.Session()
        s.send(apiRequest.prepare())

    static = media_da.get("static")
    response = Response(static, mimetype='video/webm',
                        content_type='video/webm')
    return response


@app_media.route('/media/index')
def index():
    media_path_dictionary, media_length_dictionary = MediaFileService.get_media_indexes()
    s = requests.Session()

    for item in media_path_dictionary.items():
        media_path_da.hset(item[0], item[1])

    for item in media_length_dictionary.items():
        media_length_da.hset(item[0], item[1])

    for item in media_path_dictionary.items():
        s.send(ffmpeg_request_factory.get_thumb(item[0]).prepare())
        s.send(ffmpeg_request_factory.get_meta(item[0]).prepare())

    return Response(status=200)


@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
