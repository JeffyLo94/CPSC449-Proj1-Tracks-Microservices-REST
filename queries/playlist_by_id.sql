-- :name playlist_by_id :one
SELECT * FROM playlists
WHERE id =:id;