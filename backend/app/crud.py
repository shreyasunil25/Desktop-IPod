from sqlalchemy.orm import Session
from app.models import LikedTrack, Track, RecentPlay
from collections import Counter

def get_saved_tracks(db: Session, user_id: int):
    return db.query(Track).join(LikedTrack, LikedTrack.track_id == Track.id).filter(LikedTrack.user_id == user_id).all()

def log_play(db: Session, user_id: int, track_id: int):
    play = RecentPlay(user_id=user_id, track_id=track_id)
    db.add(play)
    db.commit()
    db.refresh(play)
    return play

def get_recent_plays(db: Session, user_id: int, limit: int = 10):
    return db.query(RecentPlay).filter(RecentPlay.user_id == user_id).order_by(RecentPlay.played_at.desc()).limit(limit).all()
from sqlalchemy.orm import Session
from app.models import LikedTrack, Track, RecentPlay
from collections import Counter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

def get_saved_tracks(db: Session, user_id: int):
    return db.query(Track).join(LikedTrack, LikedTrack.track_id == Track.id).filter(LikedTrack.user_id == user_id).all()

def log_play(db: Session, user_id: int, track_id: int):
    play = RecentPlay(user_id=user_id, track_id=track_id)
    db.add(play)
    db.commit()
    db.refresh(play)
    return play

def get_recent_plays(db: Session, user_id: int, limit: int = 10):
    return db.query(RecentPlay).filter(RecentPlay.user_id == user_id).order_by(RecentPlay.played_at.desc()).limit(limit).all()

def get_recommendations(db: Session, user_id: int, limit: int = 20):
    all_tracks = db.query(Track).all()
    if not all_tracks:
        return []

    liked_ids = [r.track_id for r in db.query(LikedTrack.track_id).filter(LikedTrack.user_id == user_id).all()]
    recent = db.query(RecentPlay).filter(RecentPlay.user_id == user_id).order_by(RecentPlay.played_at.desc()).limit(20).all()
    recent_ids = [r.track_id for r in recent]

    artists = [t.artist or '' for t in all_tracks]
    genres = [t.genre or '' for t in all_tracks]

    ae = LabelEncoder().fit(artists)
    ge = LabelEncoder().fit(genres)

    track_ids = [t.id for t in all_tracks]
    features = np.array([
        [
            ae.transform([t.artist or ''])[0],
            ge.transform([t.genre or ''])[0],
            1 if t.id in liked_ids else 0,
            1 if t.id in recent_ids else 0
        ]
        for t in all_tracks
    ], dtype=float)

    if not liked_ids and not recent_ids:
        return all_tracks[:limit]

    known_ids = list(set(liked_ids + recent_ids))
    known_indices = [i for i, tid in enumerate(track_ids) if tid in known_ids]
    user_profile = features[known_indices].mean(axis=0).reshape(1, -1)

    sims = cosine_similarity(user_profile, features)[0]

    for i, tid in enumerate(track_ids):
        if tid in liked_ids:
            sims[i] += 0.3
        if tid in recent_ids:
            sims[i] -= 0.2

    ranked = sorted(zip(sims, all_tracks), key=lambda x: x[0], reverse=True)
    return [t for _, t in ranked][:limit]