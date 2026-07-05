const playBtn = document.getElementById("playBtn");
const audioPlayer = document.getElementById("audioPlayer");

playBtn.addEventListener("click", async () => {
  try {
    if (audioPlayer.paused) await audioPlayer.play();
    else audioPlayer.pause();
  } catch (err) {
    console.error("Playback error:", err);
  }
});

// Like individual song
const likeBtn = document.getElementById("likeBtn");
const likeIcon = document.getElementById("likeIcon");
let liked = false;

likeBtn.addEventListener("click", async () => {
    liked = !liked;
    likeIcon.src = liked ? "./assets/parts/liked.png" : "./assets/parts/like.png";

    const song = songs[currentIndex];
    const method = liked ? 'POST' : 'DELETE';
    await fetch(`http://127.0.0.1:8000/liked-tracks/1/${song.id}`, { method });
});

// Queue mode
let songs = [];
let currentIndex = 0;
let mode = 'recommended';
let likedQueueActive = false;

async function loadSongs(selectedMode) {
    mode = selectedMode;
    const url = mode === 'liked'
        ? 'http://127.0.0.1:8000/liked-tracks/1'
        : 'http://127.0.0.1:8000/recommendations/1';
    const res = await fetch(url);
    songs = await res.json();
    currentIndex = 0;
    playSong(currentIndex);
}

async function playSong(index) {
    const song = songs[index];
    audioPlayer.src = `http://127.0.0.1:8000/static/audio/${song.audio_url.split('/').pop()}`;
    audioPlayer.play();
    fetch(`http://127.0.0.1:8000/plays/1/${song.id}`, { method: 'POST' });

    const res = await fetch(`http://127.0.0.1:8000/liked-tracks/1/${song.id}`);
    const data = await res.json();
    liked = data.liked;
    likeIcon.src = liked ? "./assets/parts/liked.png" : "./assets/parts/like.png";

    likedQueueIcon.src = mode === 'liked'
        ? "./assets/parts/playingliked.png"
        : "./assets/parts/playliked.png";
    console.log('src:', audioPlayer.src);
}
document.getElementById('nextBtn').onclick = () => {
    currentIndex = (currentIndex + 1) % songs.length;
    playSong(currentIndex);
};

document.getElementById('prevBtn').onclick = () => {
    currentIndex = (currentIndex - 1 + songs.length) % songs.length;
    playSong(currentIndex);
};

// Liked queue toggle
const likedQueueBtn = document.getElementById("likedQueueBtn");
const likedQueueIcon = document.getElementById("likedQueueIcon");

likedQueueBtn.addEventListener("click", () => {
    likedQueueActive = !likedQueueActive;
    likedQueueIcon.src = likedQueueActive
        ? "./assets/parts/playingliked.png"   
        : "./assets/parts/playliked.png";      
    loadSongs(likedQueueActive ? 'liked' : 'recommended');
});

loadSongs('recommended');