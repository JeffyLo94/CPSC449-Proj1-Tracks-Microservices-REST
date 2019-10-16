-- :name create_playlist :insert
INSERT INTO playlists(title, urls, creator, description)
VALUES(:title, :urls, :creator, :description)