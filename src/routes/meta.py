from flask import Blueprint, Response
from utils.media_services import get_meta_url
from utils.prom_services import count_meta
import requests
import logging

app_meta = Blueprint('app_meta',__name__)

CHUNK_SIZE = 2 ** 25

@app_meta.route('/meta/<string:id>')
def meta(id):
    logging.info(f"Handling meta/{id}")
    count_meta()
    metaUrl=get_meta_url(id)
    
    req = requests.get(
        metaUrl
        )
    
    response = Response(req.iter_content(CHUNK_SIZE), content_type=req.headers['Content-Type'])
    return response

@app_meta.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

