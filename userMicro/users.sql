-- $ sqlite3 users.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER primary key,
  username VARCHAR,
  password VARCHAR,
  displayname VARCHAR,
  email VARCHAR,
  url VARCHAR,
  UNIQUE(username, displayname, email)
);

INSERT INTO users(username,password,displayname,email) VALUES('helloworld','goodbyeworld','hw','hellobyte@gmail.com');
INSERT INTO users(username,password,displayname,email) VALUES('myadd','mysub','addOrSub','actualSub''@gmail.com');
INSERT INTO users(username,password,displayname,email) VALUES('usernaming','passwording','person','user4pass@yahoo.com');
INSERT INTO users(username,password,displayname,email) VALUES('somePerson','trickingYou','another','anotherPerson3@gmail.com');
INSERT INTO users(username,password,displayname,email) VALUES('dinosaur','rawwwrs34234','dinoAge','dinosaurus@yahoo.com');
INSERT INTO users(username,password,displayname,email) VALUES('getchn','192837465','serverAdmin','getchn99@REST.microservices.gov');
INSERT INTO users(username,password,displayname,email) VALUES('studentForNow','ASDFGHJKLqwertyuiop','student1','OneStudent@csu.fullerton.edu');
INSERT INTO users(username,password,displayname,email) VALUES('studentAgain','ZXCVBNM987654321','student2','TwoStudent@csu.fullerton.edu');
INSERT INTO users(username,password,displayname,email) VALUES('studentBefore','MyPasswordIsThis','student3','ThreeStudent@csu.fullerton.edu');
INSERT INTO users(username,password,displayname,email) VALUES('studentLast','RandomPasswordHere','student4','FourStudent@csu.fullerton.edu');
INSERT INTO users(username,password,displayname,email) VALUES('studentLies','InsertPassword','student6','SixStudent@csu.fullerton.edu');
INSERT INTO users(username,password,displayname,email) VALUES('notStudent','SomethingYouCantGuess','noStudent','actualStudent@csu.fullerton.edu');
INSERT INTO users(username,password,displayname,email) VALUES('plentyOfPeople','AllofUsArePass','committee','peopleCommittee@gmail.com');
INSERT INTO users(username,password,displayname,email) VALUES('exampleUser','examplePassword','example','example@yahoo.com');
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);
-- INSERT INTO users(username,password,displayname,email) VALUES(,,,);

COMMIT;
