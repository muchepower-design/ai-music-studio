import os
import subprocess
import uuid
from .hf_client import HuggingFaceClient
from ..config import STORAGE_PATH, HF_TOKEN

class MusicGenerator:
    def __init__(self):
        self.client = HuggingFaceClient(HF_TOKEN)
    
    def generate_instrumental(self, prompt: str, duration: int, task_id: str) -> str:
        audio_bytes = self.client.generate_instrumental(prompt, duration)
        temp_path = os.path.join(STORAGE_PATH, "temp", f"{task_id}_inst.wav")
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)
        return temp_path
    
    def add_vocals(self, instrumental_path: str, lyrics: str, task_id: str) -> str:
        vocal_bytes = self.client.generate_vocals(lyrics, "")
        vocal_path = os.path.join(STORAGE_PATH, "temp", f"{task_id}_vocals.wav")
        with open(vocal_path, "wb") as f:
            f.write(vocal_bytes)
        
        mixed_path = os.path.join(STORAGE_PATH, "temp", f"{task_id}_mixed.wav")
        cmd = ['ffmpeg', '-i', instrumental_path, '-i', vocal_path,
               '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=longest',
               '-y', mixed_path]
        subprocess.run(cmd, capture_output=True)
        return mixed_path
    
    def convert_to_mp3(self, input_path: str, output_path: str):
        subprocess.run(['ffmpeg', '-i', input_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', '-y', output_path])