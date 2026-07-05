from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_saved_tracks
from app.schemas import TrackOut
from app.models import LikedTrack
router = APIRouter()

@router.get("/liked-tracks/{user_id}", response_model=list[TrackOut])
def read_saved_tracks(user_id: int, db: Session = Depends(get_db)):
    return get_saved_tracks(db, user_id)

@router.post("/liked-tracks/{user_id}/{track_id}")
def add_liked_track(user_id: int, track_id: int, db: Session = Depends(get_db)):
    from app.models import LikedTrack
    existing = db.query(LikedTrack).filter_by(user_id=user_id, track_id=track_id).first()
    if not existing:
        db.add(LikedTrack(user_id=user_id, track_id=track_id))
        db.commit()
    return {"status": "ok"}

@router.delete("/liked-tracks/{user_id}/{track_id}")
def remove_liked_track(user_id: int, track_id: int, db: Session = Depends(get_db)):
    db.query(LikedTrack).filter_by(user_id=user_id, track_id=track_id).delete()
    db.commit()
    return {"status": "ok"}

@router.get("/liked-tracks/{user_id}/{track_id}")
def is_liked(user_id: int, track_id: int, db: Session = Depends(get_db)):
    exists = db.query(LikedTrack).filter_by(user_id=user_id, track_id=track_id).first()
    return {"liked": bool(exists)}