-- $ sqlite3 descriptions.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
  id INTEGER primary key,
  user VARCHAR.
  trackurl VARCHAR,
  description VARCHAR,
  UNIQUE(user)
);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
-- INSERT INTO descriptions(user,trackurl,description) VALUES(,,);
