initDB: sqlite3 trackmeet.db < trackmeet.sql; sqlite3 track1.db < track1.sql; sqlite3 track2.db < track2.sql; sqlite3 track3.db < track3.sql

Tracks: FLASK_APP=services/tracks.py flask run -p $PORT

Playlists: FLASK_APP=services/playlists.py flask run -p $PORT

Users: FLASK_APP=services/users.py flask run -p $PORT

Descriptions: FLASK_APP=services/descriptions.py flask run -p $PORT

XSPF: FLASK_APP=services/xspf_service.py flask run -p $PORT