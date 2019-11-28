-- :name track_by_guid :one
SELECT * FROM tracks
WHERE guid = :guid;
