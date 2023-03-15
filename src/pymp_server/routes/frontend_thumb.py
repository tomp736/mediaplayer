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

app_frontend_thumb = Blueprint('app_frontend_thumb', __name__)

@app_frontend_thumb.route('/api/thumb/<string:media_id>')
def get_media_thumb(media_id):
    media_thumb = MEDIA_SERVICE.get_media_thumb(media_id)
    return Response(media_thumb, content_type="image/png")
