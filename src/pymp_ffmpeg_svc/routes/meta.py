from flask import Blueprint, Response
from ..services.MetaService import MetaService

app_meta = Blueprint('app_meta',__name__)

@app_meta.route('/meta/<string:id>', methods=['GET'])
def get_meta(id):  
    meta = MetaService.get_meta(id)
    with open(meta, 'r') as f:        
        response=Response(f.read(), 200, mimetype="application/json")
        return response


@app_meta.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response