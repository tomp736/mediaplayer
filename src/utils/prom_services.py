from prometheus_client import Counter

cv = Counter(f"request_video_total", "The total number of requests to video id.")
cvl = Counter(f"request_video_list_total", "The total number of requests to video list.")
ct = Counter(f"request_thumb_total", "The total number of requests to thumb id.")

def count_video():
    cv.inc()
    
def count_video_list():
    cvl.inc()
    
def count_thumb():
    ct.inc()