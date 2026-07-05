INSERT INTO users (name, email) VALUES ('Demo User', 'demo@example.com');

INSERT INTO tracks (title, artist, album, genre, duration_ms, audio_url) VALUES
('Track 1', 'Artist A', 'Album 1', 'Pop', 200000, '/static/audio/track1.mp3'),
('Track 2', 'Artist B', 'Album 2', 'Rock', 210000, '/static/audio/track2.mp3'),
('Track 3', 'Artist A', 'Album 3', 'Pop', 195000, '/static/audio/track3.mp3');

INSERT INTO liked_tracks (user_id, track_id) VALUES (1, 1), (1, 2);
