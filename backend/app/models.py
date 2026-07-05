from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    genre = Column(String)
    duration_ms = Column(Integer)
    audio_url = Column(String)
    source_type = Column(String, default="remote")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LikedTrack(Base):
    __tablename__ = "liked_tracks"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), primary_key=True)

class RecentPlay(Base):
    __tablename__ = "recent_plays"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    played_at = Column(DateTime(timezone=True), server_default=func.now())