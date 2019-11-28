-- :name delete_by_guid :one
DELETE FROM tracks
WHERE guid = :guid;