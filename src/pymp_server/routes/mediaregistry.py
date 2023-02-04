import json
import logging
import uuid
from flask import Response
from flask import request
from flask import Blueprint

from pymp_common.app.Services import media_registry_service
from pymp_common.dto.MediaRegistry import MediaInfo, ServiceInfo

app_mediaregistry = Blueprint('app_mediaregistry', __name__)


@app_mediaregistry.route('/registry/service')
def get_registry_service_list():
    service_infos = media_registry_service.get_registered_services()
    return Response(json.dumps(service_infos), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/service/<string:service_id>')
def get_registry_service(service_id):
    service_infos = media_registry_service.get_registered_services()
    service_info = service_infos[service_id]
    return Response(json.dumps(service_info), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/service', methods=['POST'])
def post_registry_service():
    if request.json:
        service_info = ServiceInfo()
        service_info.service_id = request.json['service_id']
        service_info.service_type = request.json['service_type']
        service_info.service_proto = request.json['service_proto']
        service_info.service_host = request.json['service_host']
        service_info.service_port = request.json['service_port']

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
    media_infos = media_registry_service.get_media_index()
    media_ids = []
    if media_infos:
        for media_id in media_infos:
            media_ids.append(media_id)
    return Response(json.dumps(media_ids), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media/<string:media_id>')
def get_registry_media(media_id):
    media_info = media_registry_service.get_media_info(media_id)
    return Response(json.dumps(media_info), status=200, content_type="application/json")


@app_mediaregistry.route('/registry/media')
def post_registry_media():
    if request.json:
        media_info = MediaInfo()
        media_info.media_id = request.json['media_id']
        media_info.service_id = request.json['service_id']
        media_registry_service.register_media(media_info)
        return Response({
            "success": True
        })

    return Response({
        "success": False
    }, status=400)


@app_mediaregistry.route('/registry/media/index')
def get_registry_media_index():
    media = media_registry_service.get_media_index()
    if not media is None:
        return Response(json.dumps(media), status=200, content_type="application/json")

    return Response(status=503)


@app_mediaregistry.after_request
def after_request(response):
    return response
