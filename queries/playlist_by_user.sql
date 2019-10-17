-- :name playlist_by_user :many
SELECT * FROM playlists
WHERE creator = :creator