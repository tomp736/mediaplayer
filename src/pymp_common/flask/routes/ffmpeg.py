from flask import Blueprint, Response

from ...app.FfmpegService import ffmpeg_service

app_ffmpeg_meta = Blueprint('app_ffmpeg_meta', __name__)
app_ffmpeg_thumb = Blueprint('app_ffmpeg_thumb', __name__)


@app_ffmpeg_meta.route('/ffmpeg/meta/<string:id>', methods=['GET'])
def ffmpeg_meta(id):
    if ffmpeg_service.process_meta(id):
        return Response(status=200)    
    return Response(status=400)

@app_ffmpeg_thumb.route('/ffmpeg/thumb/<string:id>', methods=['GET'])
def ffmpeg_thumb(id):    
    if ffmpeg_service.process_thumb(id):
        return Response(status=200)    
    return Response(status=400)
