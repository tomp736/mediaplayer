import json
import uuid
from flask import Response
from flask import request
from flask import Blueprint

from pymp_common.app.Services import media_registry_providers
from pymp_common.dto.MediaRegistry import ServiceInfo

app_mediaregistry = Blueprint('app_mediaregistry', __name__)

media_registry_provider = list(media_registry_providers.values())[0]


@app_mediaregistry.route('/registry/service', methods=['POST'])
def post_registry_service():
    service_info = ServiceInfo(**request.get_json())

    if service_info.service_id == "":
        service_info.service_id = str(uuid.uuid4())

    if not service_info is None:
        media_registry_provider.set_service_info(
            service_info.service_id, service_info)
        return Response({
            "service_id": service_info.service_id,
            "success": True
        })

    return Response({
        "service_id": service_info.service_id,
        "success": False
    }, status=400)


# @app_mediaregistry.route('/registry/service/list')
# def registry_list():
#     mediaServices = media_registry_provider.get_service_info()
#     media_svc_dict = {}
#     for media_svc_key in mediaServices.keys():
#         media_svc_dict[media_svc_key] = json.loads(
#             mediaServices[media_svc_key])
#     return Response(json.dumps(media_svc_dict), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media/list')
def list():
    mediaIndex = media_registry_provider.get_media_index()
    mediaIds = []
    if mediaIndex:
        for media_id in mediaIndex:
            mediaIds.append(media_id)
    return Response(json.dumps(mediaIds), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media/index')
def registry_media_index():
    media = media_registry_provider.get_media_index()
    if not media is None:
        return Response(json.dumps(media), status=200, content_type="application/json")

    return Response(status=503)


@app_mediaregistry.after_request
def after_request(response):
    return response
