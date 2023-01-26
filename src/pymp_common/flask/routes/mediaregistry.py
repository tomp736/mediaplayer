import json
import logging
from flask import Response, request, Blueprint
import requests

from ...dataaccess.redis import media_service_da, media_source_da
from ...dataaccess.http_request_factory import media_request_factory

app_mediaregistry = Blueprint('app_mediaregistry', __name__)


@app_mediaregistry.route('/registry/register', methods=['POST'])
def post_registry_register():
    json_data = request.get_json()
    if not json_data is None:
        media_svc_id = json_data["id"]
        media_svc_scheme = json_data["scheme"]
        media_svc_host = json_data["host"]
        media_svc_port = json_data["port"]
        media_svc_url = f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"
        mediaListRequest = media_request_factory._get_media_list_(media_svc_url)        
        try:
            s = requests.Session()
            mediaListResponse = s.send(mediaListRequest.prepare())
            if mediaListRequest and mediaListResponse.status_code == 200:                
                media_service_da.hset(
                    media_svc_id,
                    media_svc_scheme,
                    media_svc_host,
                    media_svc_port
                    )             
            return Response(status=200)
        except Exception as ex:
            logging.info(ex)
            if media_service_da.hhas(media_svc_id):
                media_service_da.hdel(media_svc_id) 
        
    return Response(status=400)

@app_mediaregistry.route('/registry/list')
def registry_list():
    media_services = media_service_da.hgetall()
    if not media_services is None:
        media_svc_dict = {}
        for media_svc_key in media_services.keys():
            media_svc_dict[media_svc_key] = json.loads(media_services[media_svc_key])
        return Response(json.dumps(media_svc_dict), status=200, content_type="application/json")

    return Response(status=503)

@app_mediaregistry.route('/registry/media/list')
def registry_media_list():
    media_sources = media_source_da.hgetall()
    if not media_sources is None:
        return Response(json.dumps(media_sources), status=200, content_type="application/json")

    return Response(status=503)


@app_mediaregistry.after_request
def after_request(response):
    return response
