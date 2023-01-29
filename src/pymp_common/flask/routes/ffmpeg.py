from flask import Blueprint, Response

from pymp_common.app.Services import ffmpegService

app_ffmpeg_meta = Blueprint('app_ffmpeg_meta', __name__)
app_ffmpeg_thumb = Blueprint('app_ffmpeg_thumb', __name__)


@app_ffmpeg_meta.route('/ffmpeg/meta/<string:mediaId>', methods=['GET'])
def ffmpeg_meta(mediaId):
    if ffmpegService.process_media(mediaId):
        return Response(status=200)    
    return Response(status=400)

@app_ffmpeg_thumb.route('/ffmpeg/thumb/<string:mediaId>', methods=['GET'])
def ffmpeg_thumb(mediaId):    
    if ffmpegService.process_meta(mediaId):
        return Response(status=200)    
    return Response(status=400)
