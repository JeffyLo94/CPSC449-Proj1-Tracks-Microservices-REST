-- :name delete_by_id :one
DELETE * FROM playlists
WHERE id = :id;