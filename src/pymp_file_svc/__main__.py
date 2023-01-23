from flask import Flask, render_template, request
from flask_dropzone import Dropzone
from prometheus_client import start_http_server
import requests
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.http_request_factory import media_request_factory
import logging
import uuid
import os

app = Flask(__name__)

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'video/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3000
app.config['DROPZONE_MAX_FILES'] = 30
dropzone = Dropzone(app)
    
def get_folder(filename):
    hash_value = hash(filename)
    hash_hex = hex(hash_value)
    filefolder = hash_hex[2:26]
    return filefolder
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        
        folder = "/files"
        filefolder = get_folder(file.filename)
        fileuuid = str(uuid.uuid4())   
        fullpath = os.path.join(folder, filefolder, fileuuid)
        fullslpath = os.path.join(folder, file.filename)     
        
        fullfilefolder = os.path.join(folder, filefolder)
        if not os.path.exists(fullfilefolder):
            os.makedirs(fullfilefolder)
            
        file.save(fullpath)
        
        os.symlink(f"./{filefolder}/{fileuuid}", f"{fullslpath}.tmp")
        os.rename(f"{fullslpath}.tmp", fullslpath)
        
        
        apiRequest = media_request_factory.get_media_index()
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