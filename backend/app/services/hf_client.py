import requests
import time
import os

class HuggingFaceClient:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {api_token}"}
    
    def generate_instrumental(self, prompt: str, duration: int) -> bytes:
        # Use MusicGen-small on HF
        API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": int(duration * 50)}  # rough estimate
        }
        response = requests.post(API_URL, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.content  # WAV bytes
        elif response.status_code == 503:
            # Model loading – wait
            time.sleep(2)
            return self.generate_instrumental(prompt, duration)
        else:
            raise Exception(f"HF API error: {response.text}")
    
    def generate_vocals(self, lyrics: str, genre: str) -> bytes:
        # Use Bark (suno/bark)
        API_URL = "https://api-inference.huggingface.co/models/suno/bark"
        payload = {"inputs": lyrics}
        response = requests.post(API_URL, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Bark API error: {response.text}")