-- :name delete_playlist :affected
DELETE FROM playlists(title, urls, creator, description)
VALUES(:title, :urls, :creator, :description)