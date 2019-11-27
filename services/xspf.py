import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import requests as req
import sys

# ----- URL CONSTANTS ------
TARGET_URL = 'http://localhost:8000/'
PLAYLIST_EPT = 'playlists'
TRACKS_EPT = 'tracks'
USERS_EPT = 'users'
DESC_EPT = 'desc'

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])
def debugPrint(data):
    print(data, file=sys.stderr)

# only needed for init support
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        db.create_all()
        with app.open_resource('trackmeet.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>XSPF MICROSERVICE</h1>
    <p> An API for generating XPSF playlists'''

@app.route('/xspf/generate/<int:id>', methods=['GET'])
def generate_xspf_by_id(id):
    debugPrint(id)
    pRes = playlist_request(id)
    return pRes.json(), status.HTTP_200_OK


# ------- HTML REQUESTS -------
def playlist_request(id):
    payload = {'id': id}
    # Actual url
    # url = TARGET_URL + PLAYLIST_EPT

    # Debug pre-kong url
    url = 'http://localhost:5200/' + PLAYLIST_EPT
    debugPrint(url)
    r = req.get(url, params=payload)
    debugPrint(r.url)
    debugPrint(r.json())
    return r