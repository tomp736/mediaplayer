from prometheus_client import Counter

request_video_total = Counter(f"request_video_total", "request_video_total")
request_video_list_total = Counter(f"request_video_list_total", "request_video_list_total")
request_thumb_total = Counter(f"request_thumb_total", "request_thumb_total")
request_meta_total = Counter(f"request_meta_total", "request_meta_total")

def count_video():
    request_video_total.inc()
    
def count_video_list():
    request_video_total.inc()
    
def count_thumb():
    request_thumb_total.inc()
    
def count_meta():
    request_meta_total.inc()