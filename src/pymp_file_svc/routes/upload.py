from flask import Blueprint, redirect, request
from ..utils.file_access import validate_filename, write_file
import json
import logging
import os

folder = os.environ.get('UPLOAD_FOLDER', '/files')
html_upload = ""

with open('./../templates/upload.html', 'r') as f:
    html_upload = f.read()
    
app_upload = Blueprint('app_upload',__name__)

@app_upload.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was actually uploaded
        if 'file' not in request.files:
            logging.info(f"Handling /upload file:{request}")
            return redirect(request.url)
        file = request.files['file']

        if not validate_filename(file.filename):
            logging.info(f"Handling /upload file:{file.filename}")
            return redirect(request.url)

        fileuuid = write_file(file.filename, file)
        
        return json.dumps(
            {
                "name": file.filename,
                "uuid" : fileuuid
            }), 200
    else:
        return html_upload

@app_upload.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
