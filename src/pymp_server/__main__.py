
from flask import Flask
from prometheus_client import start_http_server
import logging

from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.PympConfig import PympServer
from pymp_common.app.Services import ffmpegService
from pymp_common.app.Services import mediaRegistryService
from pymp_common.app.Services import mediaService
from pymp_common.app.Services import printServiceInfo

from pymp_server.routes.mediaregistry import app_mediaregistry
from pymp_server.routes.media import app_media
from pymp_server.routes.ffmpeg import app_ffmpeg_meta
from pymp_server.routes.ffmpeg import app_ffmpeg_thumb
from pymp_server.routes.frontend import app_frontend_media
from pymp_server.routes.frontend import app_frontend_thumb
from pymp_server.routes.frontend import app_frontend_meta

app = Flask(__name__)


def main():
    logging.getLogger().setLevel(logging.INFO)
    start_http_server(8000)

    printServiceInfo()

    # HOW TO DO SWITCH STATEMENT
    if (pymp_env.getServerType() & PympServer.MEDIA_API):
        app.register_blueprint(app_frontend_media)

    if (pymp_env.getServerType() & PympServer.THUMB_API):
        app.register_blueprint(app_frontend_thumb)

    if (pymp_env.getServerType() & PympServer.META_API):
        app.register_blueprint(app_frontend_meta)

    if (pymp_env.getServerType() & PympServer.MEDIAREGISTRY_SVC):
        mediaRegistryService.watchServices()
        app.register_blueprint(app_mediaregistry)

    if (pymp_env.getServerType() & PympServer.FFMPEG_SVC):
        ffmpegService.watchMedia()
        app.register_blueprint(app_ffmpeg_meta)
        app.register_blueprint(app_ffmpeg_thumb)

    if (pymp_env.getServerType() & PympServer.MEDIA_SVC):
        mediaService.watchMedia()
        app.register_blueprint(app_media)

    app.run(
        host=pymp_env.get("FLASK_RUN_HOST"),
        port=int(pymp_env.get("FLASK_RUN_PORT")),
        debug=False
    )


if __name__ == '__main__':
    main()
