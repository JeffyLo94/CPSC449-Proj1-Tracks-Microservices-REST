-- :name create_track :insert
INSERT INTO tracks(title, album, artist, songLength, song_url, art_url, guid)
VALUES(:title, :album, :artist, :songLength, :song_url, :art_url, :guid)
