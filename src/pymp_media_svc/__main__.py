
from flask import Flask
from prometheus_client import start_http_server
import os, logging
from pymp_common.services.ConfigService import ConfigService

from .routes.media import app_media

app = Flask(__name__)
app.register_blueprint(app_media)
    
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