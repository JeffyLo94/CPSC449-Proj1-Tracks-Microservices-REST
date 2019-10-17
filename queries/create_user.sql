-- :name create_user :insert
INSERT INTO users(username, password, displayname, email)
VALUES(:username, :password, :displayname, :email);
