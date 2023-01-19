from ..services.FfmpegService import FfmpegService

from pymp_common.services.RedisServices import MediaThumbService, MediaPathService
        
class ThumbService:
                
    @staticmethod
    def get_thumb(id) -> str:        
        media_thumb_c = MediaThumbService.get_redis()
        media_thumb = ""
        if not MediaThumbService.has_media_thumb(media_thumb_c, id):
            media_path_c = MediaPathService.get_redis()
            media_path_index=MediaPathService.get_media_path_index(media_path_c)
            media_path=media_path_index.get(id) or ""
            media_thumb = FfmpegService.generate_metathumb(media_path)
            MediaThumbService.set_media_thumb(media_thumb_c, id, media_thumb)
        else:
            media_thumb = MediaThumbService.get_media_thumb(media_thumb_c, id) or ""
            
        return media_thumb        
