-- :name delete_playlist :delete
DELETE FROM playlists(title, urls, creator, description)
VALUES(:title, :urls, :creator, :description)