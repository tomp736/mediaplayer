from flask import render_template, Blueprint
import requests
from pymp_common.dataaccess.http_request_factory import media_request_factory
from pymp_common.app.PympConfig import pymp_env

app_base = Blueprint('app_base',__name__)

@app_base.route('/')
def index():        
    media_host = pymp_env.media_public_fqdn()
    thumb_host = pymp_env.thumb_public_fqdn()
    meta_host = pymp_env.meta_public_fqdn()
    
    apiRequest = media_request_factory.get_media_list()    
    s = requests.Session()
    apiResponse = s.send(apiRequest.prepare())    
    ids = apiResponse.json()
    
    return render_template(
        'index.html', 
        rendered_video=render_template("video.html", src=f"{media_host}/media/static"), 
        rendered_library=render_template("library.html", ids=ids),
        media_host = media_host,
        thumb_host = thumb_host,
        meta_host = meta_host
    )

@app_base.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response