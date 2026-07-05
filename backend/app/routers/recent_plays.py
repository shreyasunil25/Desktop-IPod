from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import log_play, get_recent_plays
from app.schemas import RecentPlayOut

router = APIRouter()

@router.post("/plays/{user_id}/{track_id}")
def record_play(user_id: int, track_id: int, db: Session = Depends(get_db)):
    return log_play(db, user_id, track_id)

@router.get("/plays/{user_id}", response_model=list[RecentPlayOut])
def read_recent_plays(user_id: int, db: Session = Depends(get_db)):
    return get_recent_plays(db, user_id)