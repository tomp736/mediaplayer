from flask import Response, request, Blueprint
from utils.net_services import get_video_url
from utils.prom_services import count_video
import requests
import logging

app_video = Blueprint('app_video',__name__)

CHUNK_SIZE = 2 ** 25

@app_video.route('/video/<string:id>')
def video(id):
    logging.info(f"Handling video/{id}")
    count_video()
    videoUrl=get_video_url(id)
    
    req = requests.get(
        videoUrl, 
        stream=True,
        headers=request.headers
        )
    
    response = Response(req.iter_content(CHUNK_SIZE), 206, mimetype='video/webm', content_type='video/webm', direct_passthrough=True )
    response.headers.add('Content-Range', req.headers['Content-Range'])
    return response
