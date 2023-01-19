from flask import Blueprint, Response
from pymp_common.services.RedisServices import MediaThumbService

app_thumb = Blueprint('app_thumb',__name__)

@app_thumb.route('/thumb/<string:id>')
def thumb(id):
    r=MediaThumbService.get_redis()
    media_meta = MediaThumbService.get_media_thumb(r,id)
    response = Response(media_meta)
    return response

@app_thumb.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response