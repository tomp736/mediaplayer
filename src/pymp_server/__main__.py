
from flask import Flask
from prometheus_client import start_http_server
import logging

from pymp_core.app.config import pymp_env
from pymp_core.dto.MediaRegistry import PympServiceType

from pymp_core.app.services import MEDIA_REGISTRY_SERVICE, MEDIA_SERVICE, FFMPEG_SERVICE

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

    # HOW TO DO SWITCH STATEMENT
    if pymp_env.is_this_service_type(PympServiceType.MEDIA_API):
        app.register_blueprint(app_frontend_media)

    if pymp_env.is_this_service_type(PympServiceType.THUMB_API):
        app.register_blueprint(app_frontend_thumb)

    if pymp_env.is_this_service_type(PympServiceType.META_API):
        app.register_blueprint(app_frontend_meta)

    if pymp_env.is_this_service_type(PympServiceType.MEDIAREGISTRY_SVC):
        MEDIA_REGISTRY_SERVICE.watch_services()
        app.register_blueprint(app_mediaregistry)

    if pymp_env.is_this_service_type(PympServiceType.FFMPEG_SVC):
        FFMPEG_SERVICE.watch_media()
        app.register_blueprint(app_ffmpeg_meta)
        app.register_blueprint(app_ffmpeg_thumb)

    if pymp_env.is_this_service_type(PympServiceType.MEDIA_SVC):
        MEDIA_SERVICE.watch_media()
        app.register_blueprint(app_media)

    app.run(
        host=pymp_env.get("FLASK_RUN_HOST"),
        port=int(pymp_env.get("FLASK_RUN_PORT")),
        debug=False
    )


if __name__ == '__main__':
    main()
