--  :name change_pass :affected
UPDATE users
SET password = :password
WHERE id = :id
