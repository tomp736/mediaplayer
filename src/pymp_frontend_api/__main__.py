
from flask import Flask
from prometheus_client import start_http_server
import os
import logging

from .routes import media, thumb, meta
from pymp_common.services.ConfigService import ConfigService

app = Flask(__name__)
app.register_blueprint(media.app_video)
app.register_blueprint(thumb.app_thumb)
app.register_blueprint(meta.app_meta)
    
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