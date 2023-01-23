import sys
from flask import Blueprint, Response

from pymp_common.dataaccess.redis import media_length_da
from pymp_common.dataaccess.redis import media_da

from ..services.FfmpegService import ffmpeg_service

app_media = Blueprint('app_media', __name__)


@app_media.route('/media/<string:id>')
def get_media(id):
    if id == "static":
        video = ffmpeg_service.generate_static()
        media_length_da.hset(id, sys.getsizeof(video))
    else:
        return Response(status=404)

    media_da.set(id, video.getvalue())
    return Response(status=200)
