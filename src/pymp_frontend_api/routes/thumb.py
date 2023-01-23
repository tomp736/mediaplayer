from flask import Response, Blueprint
import requests
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.redis import media_thumb_da
from pymp_common.dataaccess.http_request_factory import ffmpeg_request_factory

app_thumb = Blueprint('app_thumb', __name__)


@app_thumb.route('/thumb/<string:id>')
def thumb(id):
    if not media_thumb_da.has(id):
        apiRequest = ffmpeg_request_factory.get_thumb(id)
        s = requests.Session()
        s.send(apiRequest.prepare())

    media_thumb = media_thumb_da.get(id)
    return Response(media_thumb, content_type="image/png")


@app_thumb.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Access-Control-Allow-Origin',
                         pymp_env.get("FEAPI_CORS_HEADER"))
    return response
