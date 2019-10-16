-- :name create_playlist :insert
INSERT INTO playlists(title, urls, user, description)
VALUES(:title, :urls, :user, :description)