import io
import logging
import ffmpeg
import json

from pymp_common.app.PympMetrics import prometheus


class FfmpegService:

    def generate_static(self) -> io.BytesIO:
        prometheus.Count("ffmpeg_static_gen_total")
        out, _ = (
            ffmpeg
            .input('smptebars=s=640x480:d=5', f='lavfi')
            .output('pipe:', format='webm', pix_fmt='rgb24')
            .run(capture_stdout=True)
        )
        return io.BytesIO(out)

    def generate_meta(self, file_path: str) -> str:
        prometheus.Count("ffmpeg_meta_gen_total")
        media_meta = ""
        try:
            media_meta = json.dumps(ffmpeg.probe(file_path)['streams'][0])
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta

    def generate_thumb(self, file_path: str) -> io.BytesIO:
        prometheus.Count("ffmpeg_thumb_gen_total")
        width = 300
        out, _ = (
            ffmpeg
            .input(file_path, ss=2)
            .filter('scale', width, -1)
            .output('pipe:', vframes=1, format='image2')
            .run(capture_stdout=True)
        )
        return io.BytesIO(out)


ffmpeg_service = FfmpegService()
