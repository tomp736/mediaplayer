

from pymp_common.abstractions.providers import FfmpegProvider


class FfmpegProviderRemote(FfmpegProvider):
    def gen_thumb(self, mediaId) -> bool:
        return False

    def gen_meta(self, mediaId) -> bool:
        return False

    def get_thumb(self, mediaId) -> bool:
        return False

    def get_meta(self, mediaId) -> bool:
        return False
