from flask import Blueprint
from flask import Response

from pymp_common.app.Services import ffmpegService

app_ffmpeg_meta = Blueprint('app_ffmpeg_meta', __name__)
app_ffmpeg_thumb = Blueprint('app_ffmpeg_thumb', __name__)


@app_ffmpeg_meta.route('/ffmpeg/meta/<string:media_id>', methods=['GET'])
def ffmpeg_meta(media_id):
    if ffmpegService.process_media(media_id):
        return Response(status=200)    
    return Response(status=400)

@app_ffmpeg_thumb.route('/ffmpeg/thumb/<string:media_id>', methods=['GET'])
def ffmpeg_thumb(media_id):    
    if ffmpegService.process_meta(media_id):
        return Response(status=200)    
    return Response(status=400)
