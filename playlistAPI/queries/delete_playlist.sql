-- :name delete_playlist :one
DELETE * FROM playlists WHERE title = :title, creator = :creator;