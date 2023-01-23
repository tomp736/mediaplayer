from typing import Dict
import os


class PympEnv:

    def __init__(self):
        self.getkeys = {
            'REDIS_HOST': "",
            'REDIS_PORT': "80",

            'MEDIA_SCHEME': "http",
            'MEDIA_HOST': "",
            'MEDIA_PORT': "80",
            'MEDIA_HOST_PUBLIC': "",
            'MEDIA_PORT_PUBLIC': "",

            'THUMB_SCHEME': "http",
            'THUMB_HOST': "",
            'THUMB_PORT': "80",
            'THUMB_HOST_PUBLIC': "",
            'THUMB_PORT_PUBLIC': "",

            'META_SCHEME': "http",
            'META_HOST': "",
            'META_PORT': "80",
            'META_HOST_PUBLIC': "",
            'META_PORT_PUBLIC': "",

            'FFMPEG_SCHEME': "http",
            'FFMPEG_HOST': "",
            'FFMPEG_PORT': "80",

            'FEAPI_CORS_HEADER': "",
            'FLASK_RUN_HOST': "0.0.0.0",
            'FLASK_RUN_PORT': "80",
            'MEDIA_CHUNK_SIZE': 2 ** 20,
            'THUMB_CHUNK_SIZE': 2 ** 10
        }

    def get(self, key: str) -> str:
        if key in self.getkeys:
            value = os.environ.get(key)
            if not value or value == "":
                value = str(self.getkeys.get(key))
            return value

        raise ValueError(f"{key} is not valid.")

    def media_fqdn(self) -> str:
        scheme = self.get("MEDIA_SCHEME")
        host = self.get("MEDIA_HOST")
        port = self.get("MEDIA_PORT")
        return f"{scheme}://{host}:{port}"

    def thumb_fqdn(self) -> str:
        scheme = self.get("THUMB_SCHEME")
        host = self.get("THUMB_HOST")
        port = self.get("THUMB_PORT")
        return f"{scheme}://{host}:{port}"

    def meta_fqdn(self) -> str:
        scheme = self.get("META_SCHEME")
        host = self.get("META_HOST")
        port = self.get("META_PORT")
        return f"{scheme}://{host}:{port}"

    def ffmpeg_fqdn(self) -> str:
        scheme = self.get("FFMPEG_SCHEME")
        host = self.get("FFMPEG_HOST")
        port = self.get("FFMPEG_PORT")
        return f"{scheme}://{host}:{port}"

    def media_public_fqdn(self) -> str:
        scheme = self.get("MEDIA_SCHEME")
        host = self.get("MEDIA_HOST_PUBLIC")
        port = self.get("MEDIA_PORT_PUBLIC")
        return f"{scheme}://{host}:{port}"

    def thumb_public_fqdn(self) -> str:
        scheme = self.get("THUMB_SCHEME")
        host = self.get("THUMB_HOST_PUBLIC")
        port = self.get("THUMB_PORT_PUBLIC")
        return f"{scheme}://{host}:{port}"

    def meta_public_fqdn(self) -> str:
        scheme = self.get("META_SCHEME")
        host = self.get("META_HOST_PUBLIC")
        port = self.get("META_PORT_PUBLIC")
        return f"{scheme}://{host}:{port}"


pymp_env = PympEnv()
