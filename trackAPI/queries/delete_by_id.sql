-- :name delete_by_id :one
DELETE * FROM tracks
WHERE id = :id;