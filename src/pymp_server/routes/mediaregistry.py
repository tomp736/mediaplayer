import json
import logging
import uuid
from flask import Response
from flask import request
from flask import Blueprint

from pymp_core.app.Services import media_registry_service
from pymp_core.dto.MediaRegistry import MediaInfo, ServiceInfo

app_mediaregistry = Blueprint('app_mediaregistry', __name__)


@app_mediaregistry.route('/registry/service')
def get_registry_service_list():
    service_infos = media_registry_service.get_registered_services()
    json_response = json.dumps(service_infos, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
    return Response(json_response, status=200, content_type="application/json")


@app_mediaregistry.route('/registry/service/<string:service_id>')
def get_registry_service(service_id):
    service_infos = media_registry_service.get_registered_services()
    service_info = service_infos[service_id]
    json_response = json.dumps(service_info, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
    return Response(json_response, status=200, content_type="application/json")


@app_mediaregistry.route('/registry/service', methods=['POST'])
def post_registry_service():
    if request.json:
        service_info = ServiceInfo.from_json(request.json)

        if service_info.service_id == "":
            service_info.service_id = str(uuid.uuid4())

        if not service_info is None:
            media_registry_service.register_service(service_info)
            return Response({
                "service_id": service_info.service_id,
                "success": True
            }, content_type="application/json")

    return Response({
        "success": False
    }, content_type="application/json", status=400)


@app_mediaregistry.route('/registry/media')
def get_registry_media_list():
    media_index = media_registry_service.get_media_index()
    json_response = json.dumps(media_index, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
    return Response(json_response, status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media/<string:media_id>')
def get_registry_media(media_id):
    media_info = media_registry_service.get_media_info(media_id)
    json_response = json.dumps(media_info, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
    return Response(json_response, status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media')
def post_registry_media():
    if request.json:
        media_info = MediaInfo.from_json(request.json)
        media_registry_service.register_media(media_info)
        return Response({
            "success": True
        })

    return Response({
        "success": False
    }, status=400)


@app_mediaregistry.route('/registry/media/index')
def get_registry_media_index():
    media_index = media_registry_service.get_media_index()
    if not media_index is None:
        json_response = json.dumps(media_index, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
        return Response(json_response, status=200, content_type="application/json")

    return Response(status=503)


@app_mediaregistry.after_request
def after_request(response):
    return response
