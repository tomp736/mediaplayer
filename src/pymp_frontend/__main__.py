
from flask import Flask
from prometheus_client import start_http_server
import os
import logging

from .routes import base
from pymp_common.app.PympConfig import pymp_env

app = Flask(__name__)
app.register_blueprint(base.app_base)
    
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