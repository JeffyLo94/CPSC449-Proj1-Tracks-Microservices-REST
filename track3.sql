-- $ sqlite3 track3.db < sqlite.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id UUID primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    songLength INT,
    song_url VARCHAR,
    art_url VARCHAR,
    UNIQUE(title, album, artist, songLength, song_url, art_url)
);
COMMIT;
