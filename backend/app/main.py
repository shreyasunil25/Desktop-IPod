from fastapi import FastAPI
from app.routers import liked_tracks, recent_plays, recommendations
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(liked_tracks.router)
app.include_router(recent_plays.router)
app.include_router(recommendations.router)

@app.get("/")
def root():
    return {"message": "iPod API is running"}

