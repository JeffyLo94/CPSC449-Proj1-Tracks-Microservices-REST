-- :name del_user_by_id :affected
DELETE FROM users
WHERE id = :id;
