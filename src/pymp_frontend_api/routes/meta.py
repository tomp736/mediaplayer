from flask import Blueprint, Response
from pymp_common.services.RedisServices import MediaMetaService

app_meta = Blueprint('app_meta',__name__)

@app_meta.route('/meta/<string:id>')
def meta(id):
    r=MediaMetaService.get_redis()
    media_meta = MediaMetaService.get_media_meta(r,id)
    response = Response(media_meta)
    return response

@app_meta.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
