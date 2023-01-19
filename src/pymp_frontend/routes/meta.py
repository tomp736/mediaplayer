from flask import Blueprint, Response
from pymp_common.services.HttpServices import FeApiService
import json

app_meta = Blueprint('app_meta',__name__)

@app_meta.route('/meta/<string:id>')
def meta(id):
    meta = FeApiService.get_meta(id)
    response = Response(json.dumps(meta), status=200, mimetype='application/json')
    return response

@app_meta.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
