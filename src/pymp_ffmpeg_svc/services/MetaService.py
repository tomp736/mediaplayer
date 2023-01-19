from ..services.FfmpegService import FfmpegService

from pymp_common.services.RedisServices import MediaMetaService, MediaPathService
        
class MetaService:
                
    @staticmethod
    def get_meta(id) -> str:
        media_meta_c = MediaMetaService.get_redis()
        media_meta = ""
        if not MediaMetaService.has_media_meta(media_meta_c, id):
            media_path_c = MediaPathService.get_redis()
            media_path_index=MediaPathService.get_media_path_index(media_path_c)
            media_path=media_path_index.get(id) or ""
            media_meta = FfmpegService.extract_file_meta(media_path)
        else:
            media_meta = MediaMetaService.get_media_meta(media_meta_c, id) or ""
            
        return media_meta        

                
