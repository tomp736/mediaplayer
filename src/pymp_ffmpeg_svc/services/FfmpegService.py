import logging
import ffmpeg
import uuid
import os
import base64
import json

class FfmpegService:
    
    @staticmethod
    def extract_file_meta(file_path:str) -> str:
        media_meta = ""
        try:
            media_meta=json.dumps(ffmpeg.probe(file_path)['streams'][0])            
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta
                
    @staticmethod
    def generate_metathumb(file_path:str) -> str:
        tmpName=str(uuid.uuid4())
        tmpPath=f"/tmp/{tmpName}.png"
        encoded_string = ""
        width = 300
        try:
            (
                ffmpeg
                .input(file_path, ss=2)
                .filter('scale', width, -1)
                .output(tmpPath, vframes=1)
                .overwrite_output()
                .run()
            )
        except ffmpeg.Error as e:
            logging.error(e.stderr.decode())
            
        if os.path.isfile(tmpPath):
            with open(tmpPath, 'rb') as f:
                encoded_string = base64.b64encode(f.read()).decode()
        
        return encoded_string