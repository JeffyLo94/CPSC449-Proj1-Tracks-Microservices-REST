-- :name delete_track :affected
DELETE FROM tracks WHERE title = :title, song_url = :song_url;