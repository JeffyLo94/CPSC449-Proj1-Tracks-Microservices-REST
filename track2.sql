-- $ sqlite3 track2.db < sqlite.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id GUID primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    songLength INT,
    song_url VARCHAR,
    art_url VARCHAR,
    UNIQUE(songLength)
);
COMMIT;
