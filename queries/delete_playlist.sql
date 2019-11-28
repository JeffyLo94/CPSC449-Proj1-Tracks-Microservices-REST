-- :name delete_playlist :affected
DELETE FROM playlists(title)
VALUES(:title)
