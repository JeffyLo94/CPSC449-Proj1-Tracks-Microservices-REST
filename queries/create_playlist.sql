-- :name create_playlist :insert
INSERT INTO playlists(title, creator, description)
VALUES(:title, :creator, :description)
