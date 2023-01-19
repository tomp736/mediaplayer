from flask import Blueprint, request, send_file
from ..utils.file_access import validate_filename, get_folder
import os
import json

folder = os.environ.get('UPLOAD_FOLDER', '/files')
html_download = ""

with open('./../templates/download.html', 'r') as f:
    html_download = f.read()
    
app_download = Blueprint('app_download',__name__)
    
@app_download.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        # Get the filename and the UUID from the request data
        data = {}
        if request.content_type == 'application/json':
            data = json.loads(request.data)
        elif request.content_type == 'application/x-www-form-urlencoded':
            data['name'] = request.form.get('name')
            data['uuid'] = request.form.get('uuid')
        else:
            return json.dumps({"error": "filename is invalid"}), 400
            
        filename = data['name']
        fileuuid = data['uuid']

        if not validate_filename(filename):
            return json.dumps({"error": "filename is invalid"}), 400
        
        # Check if the folder exists
        filefolder = get_folder(filename)
        filefolderpath = os.path.join(folder, filefolder)
        if not os.path.exists(filefolderpath):
            return json.dumps({"error": "file not found"}), 404

        # Check if the file exists
        fullpath = os.path.join(folder, filefolder, fileuuid)
        if not os.path.exists(fullpath):
            return json.dumps({"error": "file not found"}), 404

        return send_file(fullpath, as_attachment=True, download_name=filename)
    else:
        return html_download