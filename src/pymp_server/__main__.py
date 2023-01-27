
from flask import Flask
from prometheus_client import start_http_server
import logging
            
from pymp_common.flask.routes.mediaregistry import app_mediaregistry
from pymp_common.flask.routes.media import app_media
from pymp_common.flask.routes.ffmpeg import app_ffmpeg_meta, app_ffmpeg_thumb
from pymp_common.flask.routes.frontend import app_frontend_media, app_frontend_thumb, app_frontend_meta
from pymp_common.app.PympConfig import pymp_env, PympServer
from pymp_common.utils.RepeatTimer import RepeatTimer, media_loop, ffmpeg_loop, mediaregistry_loop

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

    if (server_type & PympServer.FFMPEG_SVC):
        ff_timer = RepeatTimer(60, ffmpeg_loop)
        ff_timer.start()
        app.register_blueprint(app_ffmpeg_meta)
        app.register_blueprint(app_ffmpeg_thumb)

    if (server_type & PympServer.MEDIA_SVC):
        media_timer = RepeatTimer(60, media_loop)
        media_timer.start()
        app.register_blueprint(app_media)

    if (server_type & PympServer.MEDIAREGISTRY_SVC):
        media_reg_timer = RepeatTimer(60, mediaregistry_loop)
        media_reg_timer.start()
        app.register_blueprint(app_mediaregistry)

    app.run(
        host=pymp_env.get("FLASK_RUN_HOST"),
        port=int(pymp_env.get("FLASK_RUN_PORT")),
        debug=False
    )

if __name__ == '__main__':
    main()
