-- :name create_desc :insert
INSERT INTO descriptions(user,trackurl,description)
VALUES (:user, :trackurl, :description);
