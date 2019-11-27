-- :name delete_track :affected
DELETE FROM tracks WHERE title = :title, album = :album, artist = :artist, song_url = :song_url;
