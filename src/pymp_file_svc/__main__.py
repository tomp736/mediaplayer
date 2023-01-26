import json
import random
from flask import Flask, render_template, request
from flask_dropzone import Dropzone
from prometheus_client import start_http_server
import requests
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.redis import media_source_da, media_service_da
from pymp_common.dataaccess.http_request_factory import media_request_factory
import logging
import os

app = Flask(__name__)

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'video/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3000
app.config['DROPZONE_MAX_FILES'] = 30
dropzone = Dropzone(app)
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        
        media_svc_url = None
        # check if media_source exists in redis
        if media_source_da.has():
            # get sourceid by mediaid
            media_svcs = media_service_da.hgetall()
            if media_svcs:
                media_svc = random.choice(list(media_svcs.items()))                 
                if media_svc:
                    serviceinfo = json.loads(media_svc[1])
                    media_svc_scheme = serviceinfo["scheme"]
                    media_svc_host = serviceinfo["host"]
                    media_svc_port = serviceinfo["port"]
                    media_svc_url = f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"  
                
        if media_svc_url and file and file.filename:                  
            apiRequest = media_request_factory._post_media_(media_svc_url, file.stream)
            s = requests.Session()
            s.send(apiRequest.prepare())
            return 'file uploaded successfully'
        
    return render_template('upload.html')

    
def main():
    logging.getLogger().setLevel(logging.INFO)
    start_http_server(8000)
    app.run(
        host=pymp_env.get("FLASK_RUN_HOST"), 
        port=int(pymp_env.get("FLASK_RUN_PORT")), 
        debug=False
    )

if __name__ == '__main__':
    main()