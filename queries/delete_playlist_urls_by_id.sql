-- :name delete_playlist_urls_by_id :one
DELETE FROM playlistURLs
WHERE playlistID = :id;