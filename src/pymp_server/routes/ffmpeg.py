from flask import Blueprint
from flask import Response

from pymp_core.app.Services import ffmpeg_service
from pymp_core.app.Services import media_registry_service


app_ffmpeg_meta = Blueprint('app_ffmpeg_meta', __name__)
app_ffmpeg_thumb = Blueprint('app_ffmpeg_thumb', __name__)

@app_ffmpeg_meta.route('/ffmpeg/meta/<string:media_id>', methods=['GET'])
def ffmpeg_meta(media_id):
    media_info = media_registry_service.get_media_info(media_id)
    if ffmpeg_service.process_media_meta(media_info):
        return Response(status=200)    
    return Response(status=400)

@app_ffmpeg_thumb.route('/ffmpeg/thumb/<string:media_id>', methods=['GET'])
def ffmpeg_thumb(media_id):    
    media_info = media_registry_service.get_media_info(media_id)
    if ffmpeg_service.process_media_thumb(media_info):
        return Response(status=200)    
    return Response(status=400)
