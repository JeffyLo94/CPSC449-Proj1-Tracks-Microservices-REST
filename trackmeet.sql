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
    UNIQUE(title, album, artist, songLength, song_url)
);
CREATE TABLE playlists (
    id INTEGER primary key,
    title VARCHAR,
    urls VARCHAR,
    creator VARCHAR,
    description VARCHAR,
    UNIQUE(title, creator)
);
CREATE TABLE users (
  id INTEGER primary key,
  username VARCHAR,
  password VARCHAR,
  displayname VARCHAR,
  email VARCHAR,
  url VARCHAR,
  UNIQUE(username, displayname, email)
);
CREATE TABLE descriptions (
  id INTEGER primary key,
  user VARCHAR,
  trackurl VARCHAR,
  description VARCHAR
);
COMMIT;
