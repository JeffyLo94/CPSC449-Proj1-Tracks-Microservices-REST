-- :name all_urls_for_playlist :many
SELECT URL FROM playlistURLs
WHERE playlistID = :playlistID