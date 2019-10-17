-- $ sqlite3 tracks.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
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
INSERT INTO tracks(title, album, artist, songLength, song_url, art_url) VALUES('Intro','Championships','Meek Mill', 330, 'blahblahblah.com/intro', 'blahblahblah.com/artintro');
INSERT INTO tracks(title, album, artist, songLength, song_url, art_url) VALUES('Dreams and Nightmares','Dreams and Nightmares','Meek Mill', 351, 'blahblahblah.com/dream', 'blahblahblah.com/artdream');
INSERT INTO tracks(title, album, artist, songLength, song_url, art_url) VALUES('Me You','Theres Really a Wolf','Russ', 244, 'blahblahblah.com/me', 'blahblahblah.com/artme');
INSERT INTO tracks(title, album, artist, songLength, song_url, art_url) VALUES('Gyalchester','More Life','Drake', 309, 'blahblahblah.com/gyal', 'blahblahblah.com/artgyal');
COMMIT;