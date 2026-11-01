from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from datetime import datetime
from .database import Base

class GeneratedTrack(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True)
    prompt = Column(Text)
    genre = Column(String)
    duration = Column(Integer)
    include_vocals = Column(Boolean)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)