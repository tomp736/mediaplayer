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
    logging.info(json_data)
    if not json_data is None:
        media_svc_id = json_data["id"]
        media_svc_scheme = json_data["scheme"]
        media_svc_host = json_data["host"]
        media_svc_port = json_data["port"]

        media_svc_url = f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"
        logging.info(media_svc_url)
        mediaListRequest = media_request_factory._get_media_list_(media_svc_url)
        s = requests.Session()
        mediaListResponse = s.send(mediaListRequest.prepare())
        logging.info(mediaListResponse.status_code)
        if mediaListResponse.status_code == 200:            
            redis_dict = media_source_da.hgetall()
            media_ids = []
            for media_id in mediaListResponse.json():
                media_ids.append(media_id)
            
            if not redis_dict is None:
                for redis_id in redis_dict:
                    if redis_dict[redis_id] == media_svc_id: 
                        if not media_ids.__contains__(redis_id):
                            logging.info(f"deleting: {redis_id}")
                            media_source_da.hdel(redis_id)
                    
            # populate media_id -> media_svc_id
            for media_id in media_ids:
                media_source_da.hset(media_id, media_svc_id)      
                          
            # populate media_svc_id -> media_svc_info
            media_service_da.hset(
                media_svc_id, 
                media_svc_scheme, 
                media_svc_host, 
                media_svc_port)
            
            return Response(status=200)

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
