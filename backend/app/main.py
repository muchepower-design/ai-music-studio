from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid
import os
import shutil

from .database import engine, Base, get_db
from .models import GeneratedTrack
from .schemas import GenerationRequest, GenerationResponse
from .services.music_generator import MusicGenerator
from .config import STORAGE_PATH

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Music Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

music_gen = MusicGenerator()

# Ensure storage directories exist
os.makedirs(os.path.join(STORAGE_PATH, "temp"), exist_ok=True)
os.makedirs(os.path.join(STORAGE_PATH, "outputs"), exist_ok=True)

def process_music_generation(task_id: str, request: GenerationRequest, db: Session):
    try:
        # Step 1: instrumental
        inst_path = music_gen.generate_instrumental(request.prompt, request.duration, task_id)

        final_audio = inst_path
        if request.include_vocals and request.lyrics:
            final_audio = music_gen.add_vocals(inst_path, request.lyrics, task_id)

        # Step 2: convert to MP3
        mp3_path = os.path.join(STORAGE_PATH, "outputs", f"{task_id}.mp3")
        music_gen.convert_to_mp3(final_audio, mp3_path)

        # Save to database
        track = GeneratedTrack(
            id=task_id,
            prompt=request.prompt,
            genre=request.genre.value,
            duration=request.duration,
            include_vocals=request.include_vocals,
            file_path=mp3_path
        )
        db.add(track)
        db.commit()

        # Clean temp files
        os.remove(inst_path)
        if request.include_vocals and os.path.exists(final_audio):
            os.remove(final_audio)

    except Exception as e:
        print(f"Generation failed for {task_id}: {e}")
        # You could store error status in DB if needed

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_music(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(process_music_generation, task_id, request, db)
    return GenerationResponse(
        task_id=task_id,
        status="processing",
        message="Your music is being created in the background."
    )

@app.get("/api/status/{task_id}")
async def get_status(task_id: str, db: Session = Depends(get_db)):
    track = db.query(GeneratedTrack).filter(GeneratedTrack.id == task_id).first()
    if track:
        return {
            "task_id": task_id,
            "status": "completed",
            "download_url": f"/api/download/{task_id}"
        }
    else:
        # If not in DB, either still processing or failed
        # For simplicity, assume processing if file not ready
        output_file = os.path.join(STORAGE_PATH, "outputs", f"{task_id}.mp3")
        if os.path.exists(output_file):
            return {"task_id": task_id, "status": "completed", "download_url": f"/api/download/{task_id}"}
        else:
            return {"task_id": task_id, "status": "processing"}

@app.get("/api/download/{task_id}")
async def download_track(task_id: str):
    file_path = os.path.join(STORAGE_PATH, "outputs", f"{task_id}.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=f"{task_id}.mp3")
    raise HTTPException(status_code=404, detail="Track not found")

@app.get("/api/waveform/{task_id}")
async def get_waveform(task_id: str):
    from .utils.audio_utils import get_waveform_data
    file_path = os.path.join(STORAGE_PATH, "outputs", f"{task_id}.mp3")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Track not found")
    
    # Convert mp3 to wav temporarily for processing
    import subprocess
    wav_path = file_path.replace('.mp3', '_temp.wav')
    subprocess.run(['ffmpeg', '-i', file_path, '-y', wav_path], capture_output=True)
    waveform = get_waveform_data(wav_path)
    os.remove(wav_path)
    return {"waveform": waveform}