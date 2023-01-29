import json
from flask import Response, request, Blueprint

from pymp_common.app.Services import mediaRegistryService

app_mediaregistry = Blueprint('app_mediaregistry', __name__)


@app_mediaregistry.route('/registry/register', methods=['POST'])
def post_registry_register():
    serviceInfo = request.get_json()
    if not serviceInfo is None:
        mediaRegistryService.register(serviceInfo)
        return Response(status=200)
        
    return Response(status=400)

@app_mediaregistry.route('/registry/list')
def registry_list():
    mediaServices = mediaRegistryService.getMediaServices()
    media_svc_dict = {}
    for media_svc_key in mediaServices.keys():
        media_svc_dict[media_svc_key] = json.loads(mediaServices[media_svc_key])
    return Response(json.dumps(media_svc_dict), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media/list')
def list(): 
    mediaIndex = mediaRegistryService.getMediaIndex()
    mediaIds = []
    if mediaIndex:
        for mediaId in mediaIndex:
            mediaIds.append(mediaId)
    return Response(json.dumps(mediaIds), status=200, content_type="application/json")

@app_mediaregistry.route('/registry/media/index')
def registry_media_index():
    media = mediaRegistryService.getMediaIndex()
    if not media is None:
        return Response(json.dumps(media), status=200, content_type="application/json")

    return Response(status=503)


@app_mediaregistry.after_request
def after_request(response):
    return response
