import sys
from flask import Blueprint, Response

from ...dataaccess.redis import media_da
from ...dataaccess.redis import media_path_da
from ...dataaccess.redis import media_length_da
from ...dataaccess.redis import media_meta_da
from ...dataaccess.redis import media_thumb_da

from ...app.FfmpegService import ffmpeg_service

app_ffmpeg_meta = Blueprint('app_ffmpeg_meta', __name__)
app_ffmpeg_media = Blueprint('app_ffmpeg_media', __name__)
app_ffmpeg_thumb = Blueprint('app_ffmpeg_thumb', __name__)


@app_ffmpeg_meta.route('/ffmpeg/meta/<string:id>', methods=['GET'])
def ffmpeg_meta(id):
    if media_path_da.hhas(id):
        media_path = str(media_path_da.hget(id))
        media_meta = ffmpeg_service.generate_meta(media_path)
        media_meta = media_meta_da.set(id, media_meta)
    else:
        return Response(status=404)
    return Response(status=200)

@app_ffmpeg_media.route('/ffmpeg/media/<string:id>', methods=['GET'])
def ffmpeg_media(id):
    if id == "static":
        video = ffmpeg_service.generate_static()
        media_length_da.hset(id, sys.getsizeof(video))
    else:
        return Response(status=404)

    media_da.set(id, video.getvalue())
    return Response(status=200)

@app_ffmpeg_thumb.route('/ffmpeg/thumb/<string:id>', methods=['GET'])
def ffmpeg_thumb(id):
    if media_path_da.hhas(id):
        media_path = str(media_path_da.hget(id))
        media_thumb = ffmpeg_service.generate_thumb(media_path)
        media_thumb_da.set(id, media_thumb.getvalue())
    else:
        return Response(status=404)
    return Response(status=200)
