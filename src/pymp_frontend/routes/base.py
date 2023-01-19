from flask import render_template, Blueprint
from pymp_common.services.HttpServices import FeApiService

app_base = Blueprint('app_base',__name__)

@app_base.route('/')
def index():
    ids = FeApiService.get_media_list()
    
    return render_template(
        'index.html', 
        rendered_video=render_template("video.html", src=f"/media/{ids[0]}"), 
        rendered_library=render_template("library.html", ids=ids)
    )

@app_base.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response