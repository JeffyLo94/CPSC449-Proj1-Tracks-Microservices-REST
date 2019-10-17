-- :name user_by_id :one
SELECT * FROM users
WHERE id = :id
