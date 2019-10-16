-- :name delete_playlist :insert
DELETE FROM playlists(title, urls, user, description)
VALUES(:title, :urls, :user, :description)