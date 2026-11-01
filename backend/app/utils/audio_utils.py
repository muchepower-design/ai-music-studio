import numpy as np
import soundfile as sf

def get_waveform_data(file_path: str, num_points: int = 100):
    """Extract waveform amplitudes for frontend visualization"""
    data, samplerate = sf.read(file_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1)  # convert to mono
    
    # Downsample to num_points
    indices = np.linspace(0, len(data)-1, num_points, dtype=int)
    waveform = data[indices]
    
    # Normalize to [-1, 1] range
    max_val = np.max(np.abs(waveform))
    if max_val > 0:
        waveform = waveform / max_val
    
    return waveform.tolist()