
DROP KEYSPACE IF EXISTS trackmeet;

CREATE KEYSPACE trackmeet
    WITH replication = {
      'class' : 'SimpleStrategy',
      'replication_factor' : 1
    };


CREATE TABLE tracks_playlists_desc (
    guid BLOB,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    songLength INT,
    song_url VARCHAR,
    art_url VARCHAR,

    pl_title VARCHAR,
    pl_creator VARCHAR,
    pl_desc VARCHAR,

    pl_tracks LIST<VARCHAR>,

    d_trackurl VARCHAR,
    d_description VARCHAR,

    PRIMARY KEY(guid,pl_title)
  );


CREATE TABLE users (
    id INT
    username VARCHAR,
    password VARCHAR,
    displayname VARCHAR,
    email VARCHAR,
    url VARCHAR,
    PRIMARY KEY (id)
);
