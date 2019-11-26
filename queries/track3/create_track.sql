-- :name create_track :insert
INSERT INTO tracks(title, album, artist, songLength, song_url, art_url)
VALUES(:title, :album, :artist, :songLength, :song_url, :art_url)
