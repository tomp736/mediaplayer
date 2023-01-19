from flask import Blueprint, Response
from ..services.ThumbService import ThumbService

app_thumb = Blueprint('app_thumb',__name__)

@app_thumb.route('/thumb/<string:id>')
def video_thumb(id):  
    thumb = ThumbService.get_thumb(id)
    response=Response(thumb, 200, mimetype="text")
    return response

@app_thumb.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
