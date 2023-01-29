
from flask import Flask
from prometheus_client import start_http_server
import logging
            
from pymp_common.flask.routes.mediaregistry import app_mediaregistry
from pymp_common.flask.routes.media import app_media
from pymp_common.flask.routes.ffmpeg import app_ffmpeg_meta, app_ffmpeg_thumb
from pymp_common.flask.routes.frontend import app_frontend_media, app_frontend_thumb, app_frontend_meta
from pymp_common.app.PympConfig import pymp_env, PympServer

from pymp_common.app.Services import ffmpegService, mediaRegistryService, mediaService

app = Flask(__name__)
server_type = pymp_env.getServerType()

def main():
    logging.getLogger().setLevel(logging.INFO)
    start_http_server(8000)

    logging.info(server_type)

    if (server_type & PympServer.MEDIA_API):
        app.register_blueprint(app_frontend_media)

    if (server_type & PympServer.THUMB_API):
        app.register_blueprint(app_frontend_thumb)

    if (server_type & PympServer.META_API):
        app.register_blueprint(app_frontend_meta)

    if (server_type & PympServer.MEDIAREGISTRY_SVC):
        mediaRegistryService.watchServices()
        app.register_blueprint(app_mediaregistry)
        
    if (server_type & PympServer.FFMPEG_SVC):
        ffmpegService.watchMedia()
        app.register_blueprint(app_ffmpeg_meta)
        app.register_blueprint(app_ffmpeg_thumb)

    if (server_type & PympServer.MEDIA_SVC):
        mediaService.watchMedia()
        app.register_blueprint(app_media)

    app.run(
        host=pymp_env.get("FLASK_RUN_HOST"),
        port=int(pymp_env.get("FLASK_RUN_PORT")),
        debug=False
    )

if __name__ == '__main__':
    main()
