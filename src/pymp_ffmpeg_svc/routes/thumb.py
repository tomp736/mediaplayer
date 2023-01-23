from flask import Blueprint, Response

from pymp_common.dataaccess.redis import media_path_da
from pymp_common.dataaccess.redis import media_thumb_da

from ..services.FfmpegService import ffmpeg_service

app_thumb = Blueprint('app_thumb', __name__)


@app_thumb.route('/thumb/<string:id>', methods=['GET'])
def get_thumb(id):
    if media_path_da.hhas(id):
        media_path = str(media_path_da.hget(id))
        media_thumb = ffmpeg_service.generate_thumb(media_path)
        media_thumb_da.set(id, media_thumb.getvalue())
    else:
        return Response(status=404)
    return Response(status=200)
