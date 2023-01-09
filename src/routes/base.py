from flask import render_template, Blueprint
from utils.net_services import get_video_ids
from utils.prom_services import count_video_list
import logging

app_base = Blueprint('app_base',__name__)

@app_base.route('/')
def index():
    logging.info(f"Handling /")
    count_video_list()
    ids = get_video_ids()
    
    return render_template(
        'index.html', 
        rendered_video=render_template("video.html", id=ids[0]), 
        rendered_library=render_template("library.html", ids=ids)
    )