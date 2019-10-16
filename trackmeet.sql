-- $ sqlite3 trackmeet.db < sqlite.sql

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS descriptions;
CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,       
    songLength INT,
    song_url VARCHAR,
    art_url VARCHAR,
    UNIQUE(title, album, artist, songLength, song_url, art_url)
);
CREATE TABLE playlists (
    id INTEGER primary key,
    title VARCHAR,
    urls VARCHAR,
    creator VARCHAR,
    description VARCHAR
    UNIQUE(title, creator)
);
COMMIT;