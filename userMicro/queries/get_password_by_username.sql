-- :name get_password_by_username :scalar
SELECT password FROM users
WHERE username = :username
