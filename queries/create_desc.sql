-- :name create_desc :insert
INSERT INTO descriptions(username, trackurl, description)
VALUES (:username, :trackurl, :description);
