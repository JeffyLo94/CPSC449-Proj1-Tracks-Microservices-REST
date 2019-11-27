--  :name change_pass :affected
UPDATE users
SET password = :password
WHERE username = :username
