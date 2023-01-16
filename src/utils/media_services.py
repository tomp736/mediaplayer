from typing import Dict, List
import requests
import os

video_host=os.environ.get('SVC_VIDEO_HOST', 'httpvideo')
video_port=int(os.environ.get('SVC_VIDEO_PORT', '80'))       

def get_video_url(id: str) -> str:
    return f"http://{video_host}:{video_port}/video/{id}"

def get_video_ids_url() -> str:
    return f"http://{video_host}:{video_port}/video/list"

def get_video_ids() -> List[str]:
    listUrl = get_video_ids_url()
    response = requests.get(listUrl)
    ids = response.json()
    return ids

thumb_host=os.environ.get('SVC_THUMB_HOST', 'httpthumb')
thumb_port=int(os.environ.get('SVC_THUMB_PORT', '80'))

def get_thumb_url(id: str) -> str:
    return f"http://{thumb_host}:{thumb_port}/thumb/{id}"

meta_host=os.environ.get('SVC_META_HOST', '0.0.0.0')
meta_port=int(os.environ.get('SVC_META_PORT', '80'))

def get_meta_url(id: str) -> str:
    return f"http://{meta_host}:{meta_port}/meta/{id}"

def get_video_meta(id) -> Dict[str, str]:
    metaUrl = get_meta_url(id)
    response = requests.get(metaUrl)
    metadictionary = response.json()
    return metadictionary