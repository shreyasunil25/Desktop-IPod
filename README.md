# iPod Desktop Music Player

A floating iPod-style desktop music player with offline playback, song liking, and recommendation system using cosine similarity.

## Stack
- **Frontend:** Electron, HTML, CSS, JS
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL (Docker)
- **ML:** scikit-learn, numpy

## Setup

**1. Start database**
```bash
docker compose up -d
```

**2. Start backend**
```bash
cd backend
uv run uvicorn app.main:app --reload
```

**3. Add music**

Place `.mp3` files in `backend/static/audio/` and insert into DB:
```sql
INSERT INTO tracks (title, artist, album, genre, duration_ms, audio_url)
VALUES ('Title', 'Artist', 'Album', 'Genre', 210000, '/static/audio/title.mp3');
```

**4. Run app**
```bash
npm run start
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/liked-tracks/{user_id}` | Get liked songs |
| POST | `/liked-tracks/{user_id}/{track_id}` | Like a song |
| DELETE | `/liked-tracks/{user_id}/{track_id}` | Unlike a song |
| GET | `/recommendations/{user_id}` | Get recommendations |
| POST | `/plays/{user_id}/{track_id}` | Log a play |

## Recommendations

Track features (artist, genre) are encoded into vectors. Cosine similarity is computed between the user's listening profile and all tracks. Liked songs are boosted, recently played ones penalized for variety.