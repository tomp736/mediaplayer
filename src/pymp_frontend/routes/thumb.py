from flask import Blueprint, Response
from pymp_common.services.HttpServices import FeApiService

app_thumb = Blueprint('app_thumb',__name__)

@app_thumb.route('/thumb/<string:id>')
def thumb(id):
    thumb = FeApiService.get_thumb(id)
    response = Response(thumb, status=200, mimetype='text')
    return response

@app_thumb.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response