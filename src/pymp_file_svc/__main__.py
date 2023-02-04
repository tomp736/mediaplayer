import json
import random
from flask import Flask
from flask import render_template
from flask import request
from flask_dropzone import Dropzone
from prometheus_client import start_http_server
import requests
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.redis import redis_media_info
from pymp_common.dataaccess.redis import redis_service_info
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
        if redis_media_info.has():
            # get sourceid by mediaid
            media_svcs = redis_service_info.hgetall()
            if media_svcs:
                media_svc = random.choice(list(media_svcs.items()))
                if media_svc:
                    serviceinfo = json.loads(media_svc[1])
                    media_svc_proto = serviceinfo["proto"]
                    media_svc_host = serviceinfo["host"]
                    media_svc_port = serviceinfo["port"]
                    media_svc_url = f"{media_svc_proto}://{media_svc_host}:{media_svc_port}"

        if media_svc_url and file and file.filename:
            apiRequest = media_request_factory._post_media_(
                media_svc_url, file.stream)
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
