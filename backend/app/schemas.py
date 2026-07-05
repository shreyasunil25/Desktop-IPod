from pydantic import BaseModel
from datetime import datetime

class TrackOut(BaseModel):
    id: int
    title: str
    artist: str
    album: str | None
    genre: str | None
    duration_ms: int | None
    audio_url: str

    model_config = {"from_attributes": True}


class RecentPlayOut(BaseModel):
    id: int
    user_id: int
    track_id: int
    played_at: datetime
    track: TrackOut | None = None

    model_config = {"from_attributes": True}