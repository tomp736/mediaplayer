from flask import Blueprint, Response
from utils.net_services import get_thumb_url
from utils.prom_services import count_thumb
import requests
import logging

app_thumb = Blueprint('app_thumb',__name__)

CHUNK_SIZE = 2 ** 25

@app_thumb.route('/thumb/<string:id>')
def thumb(id):
    logging.info(f"Handling thumb/{id}")
    count_thumb()
    thumbUrl=get_thumb_url(id)
    
    req = requests.get(
        thumbUrl
        )
    
    response = Response(req.iter_content(CHUNK_SIZE), content_type=req.headers['Content-Type'])
    return response

