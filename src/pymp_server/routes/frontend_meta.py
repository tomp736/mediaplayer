import logging
import json

from flask import Blueprint
from flask import Response
from flask import request
from flask import redirect
from pymp_core.abstractions.providers import MediaChunk
from pymp_core.app.config_factory import CONFIG_FACTORY

from pymp_core.app.services import MEDIA_SERVICE
from pymp_core.app.services import MEDIA_REGISTRY_SERVICE

app_frontend_meta = Blueprint('app_frontend_meta', __name__)

@app_frontend_meta.route('/api/meta/<string:media_id>')
def get_media_meta(media_id):
    media_meta = MEDIA_SERVICE.get_media_meta(media_id)
    if media_meta:
        return Response(media_meta)
    return {}
