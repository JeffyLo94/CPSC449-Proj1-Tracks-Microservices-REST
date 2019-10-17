--  :name change_pass :scalar
UPDATE users
SET password = :password
WHERE id = :id
