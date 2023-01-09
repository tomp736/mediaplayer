from flask import Blueprint

app_def = Blueprint('app_def',__name__)

@app_def.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response