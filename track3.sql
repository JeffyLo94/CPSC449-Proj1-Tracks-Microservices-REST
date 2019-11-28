-- $ sqlite3 track3.db < sqlite.sql

-- PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    guid GUID primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    songLength INT,
    song_url VARCHAR,
    art_url VARCHAR,
    UNIQUE(song_url)
);
COMMIT;
