import json
import logging
from flask import Response
from flask import request
from flask import Blueprint


from pymp_core.app.Services import media_service
from pymp_core.dto.Media import MediaChunk

app_media = Blueprint('app_media', __name__)

@app_media.route('/media/<string:media_id>', methods=['GET'])
def get_media(media_id):
    start_byte, end_byte, file_size = MediaChunk.parse_range_header(
        request.headers["Range"])
    media_chunk = media_service.get_media_chunk(media_id, start_byte, end_byte)
    if media_chunk:
        response = Response(
            media_chunk.chunk,
            206,
            mimetype='video/webm',
            content_type='video/webm')

        response.headers.set(
            'Content-Range', media_chunk.to_content_range_header()
        )
        logging.info(response)
        logging.info(response.headers)
        return response

    return Response(status=400)


# @app_media.route('/media', methods=['POST'])
# def post_media():
#     if request.method == 'POST':
#         if not media_service:
#             return Response(status=400)
#         media_service.save_media("output_file", request.stream)
#     return Response(status=404)


@app_media.route('/media/index', methods=['GET'])
def get_index():
    media_service.update_index()
    return Response(status=200)


@app_media.route('/media/list', methods=['GET'])
def get_list():
    media_ids = media_service.get_media_ids()
    return Response(json.dumps(media_ids), mimetype='application/json')


@app_media.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
