from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GenreEnum(str, Enum):
    COUNTRY = "country"
    HIP_HOP = "hip-hop"
    RAGGAE = "raggae"
    RHUMBA = "rhumba"
    RNB = "rnb"
    AFROBEATS = "afrobeats"

class GenerationRequest(BaseModel):
    prompt: str
    genre: GenreEnum
    duration: int = 30
    include_vocals: bool = False
    lyrics: Optional[str] = None

class GenerationResponse(BaseModel):
    task_id: str
    status: str
    message: str