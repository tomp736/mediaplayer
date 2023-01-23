from flask import Blueprint, Response

from pymp_common.dataaccess.redis import media_path_da
from pymp_common.dataaccess.redis import media_meta_da

from ..services.FfmpegService import ffmpeg_service

app_meta = Blueprint('app_meta', __name__)


@app_meta.route('/meta/<string:id>', methods=['GET'])
def get_meta(id):
    if media_path_da.hhas(id):
        media_path = str(media_path_da.hget(id))
        media_meta = ffmpeg_service.generate_meta(media_path)
        media_meta = media_meta_da.set(id, media_meta)
    else:
        return Response(status=404)
    return Response(status=200)