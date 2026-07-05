from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_recommendations
from app.schemas import TrackOut

router = APIRouter()

@router.get("/recommendations/{user_id}", response_model=list[TrackOut])
def read_recommendations(user_id: int, db: Session = Depends(get_db)):
    return get_recommendations(db, user_id)
