from flask import Flask
from prometheus_client import start_http_server
from .routes import download, upload
import os
import logging
from pymp_common.services.ConfigService import ConfigService
    
app = Flask(__name__)

app.register_blueprint(download.app_download)
app.register_blueprint(upload.app_upload)
    
def main():
    logging.getLogger().setLevel(logging.INFO)
    start_http_server(8000)
    app.run(
        host=ConfigService.flask_host, 
        port=ConfigService.flask_port, 
        debug=False
    )

if __name__ == '__main__':
    main()