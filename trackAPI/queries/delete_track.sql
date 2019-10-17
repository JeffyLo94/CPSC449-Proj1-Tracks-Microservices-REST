-- :name delete_track :delete
DELETE FROM tracks WHERE title = :title, song_url = :song_url;