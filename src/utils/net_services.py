import json
import requests

def get_thumb_url(id):
    return f"http://httpthumb/thumb/{id}"

def get_video_url(id):
    return f"http://httpvideo/video/{id}"

def get_video_ids_url():
    return f"http://httpvideo/video/list"

def get_video_ids():
    listUrl = get_video_ids_url()
    response = requests.get(listUrl)
    ids = response.json()
    return ids