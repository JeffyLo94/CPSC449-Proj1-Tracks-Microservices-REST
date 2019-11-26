-- $ sqlite3 trackmeet.db < sqlite.sql

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS playlistURLs;
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
    UNIQUE(title, album, artist, songLength, song_url)
);
CREATE TABLE playlists (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    creator VARCHAR,
    description VARCHAR,
    UNIQUE(title, creator)
    FOREIGN KEY(creator) REFERENCES users(username) ON DELETE CASCADE
);
CREATE TABLE playlistURLs (
    id INTEGER PRIMARY KEY,
    url VARCHAR,
    playlistID INTEGER,
    FOREIGN KEY(playlistID) REFERENCES playlists(id) ON DELETE CASCADE
);
CREATE TABLE users (
  id INTEGER primary key,
  username VARCHAR,
  password VARCHAR,
  displayname VARCHAR,
  email VARCHAR,
  url VARCHAR
);
CREATE TABLE descriptions (
  id INTEGER primary key,
  username VARCHAR,
  trackurl VARCHAR,
  description VARCHAR,
  FOREIGN KEY(trackurl) REFERENCES tracks(song_url) ON DELETE CASCADE
);
COMMIT;
