-- :name track_by_id :one
SELECT * FROM tracks
WHERE id = :id;
