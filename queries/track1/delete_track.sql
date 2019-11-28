-- :name delete_track :affected
DELETE FROM tracks
WHERE title = :title AND
      album = :album AND
      artist = :artist AND
      song_url = :song_url;
