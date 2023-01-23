
from flask import Flask
from prometheus_client import start_http_server
import os
import logging

from .routes import media, thumb, meta
from pymp_common.app.PympConfig import pymp_env

app = Flask(__name__)
app.register_blueprint(media.app_media)
app.register_blueprint(thumb.app_thumb)
app.register_blueprint(meta.app_meta)
    
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