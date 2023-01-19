from prometheus_client import Counter

class MetricsService:
    request_video_total = Counter(f"request_video_total", "request_video_total")
    request_video_list_total = Counter(f"request_video_list_total", "request_video_list_total")
    request_thumb_total = Counter(f"request_thumb_total", "request_thumb_total")
    request_meta_total = Counter(f"request_meta_total", "request_meta_total")
    indexed_videos_total = Counter(f"indexed_videos_total", "The total number videos returned by index.")

    @staticmethod
    def count_video():
        MetricsService.request_video_total.inc()
        
    @staticmethod
    def count_video_list():
        MetricsService.request_video_total.inc()
        
    @staticmethod
    def count_thumb():
        MetricsService.request_thumb_total.inc()
        
    @staticmethod
    def count_meta():
        MetricsService.request_meta_total.inc()
        
    @staticmethod
    def count_index():
        MetricsService.indexed_videos_total.inc()