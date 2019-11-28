-- :name edit_track :affected
UPDATE tracks set title = :title,
				  album = :album,
				  artist = :artist,
				  songLength = :songLength,
				  song_url = :song_url,
				  art_url = :art_url
WHERE guid = :guid
