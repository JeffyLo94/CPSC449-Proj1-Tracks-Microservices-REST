import flask_api
from flask_api import status
import pugsql
import requests as req
import sys
from services.modules import xspf

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

# only needed for init support
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        db.create_all()
        with app.open_resource('trackmeet.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# ----- URL CONSTANTS ------
TARGET_URL = 'http://localhost:8000/'
PLAYLIST_EPT = 'playlists'
TRACKS_EPT = 'tracks'
USERS_EPT = 'users'
DESC_EPT = 'desc'
DEBUG_MODE = True


def debugPrint(data):
    if DEBUG_MODE:
        print(data, file=sys.stderr)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>XSPF MICROSERVICE</h1>
    <p> An API for generating XPSF playlists'''

@app.route('/xspf/generate/<int:id>', methods=['GET'])
def generate_xspf_by_id(id):
    debugPrint(id)
    pRes = playlist_request(id)
    debugPrint('type')
    debugPrint(type(pRes.json()))
    jsonlist = pRes.json()
    json = jsonlist[0]
    x = xspf.Xspf()
    x.title = json['title']
    x.identifier = str(json['id'])
    x.creator = json['creator']
    x.info = json['description']
    for t_url in json['urls']:
        debugPrint(t_url)
        track_jsonlist = tracks_request(t_url)
        track_json = track_jsonlist[0]
        track = xspf.Track()
        track.title = track_json['title']
        track.identifier = track_json['guid']
        track.album = track_json['album']
        track.duration = track_json['songLength']
        track.creator = track_json['artist']
        if(track_json['art_url']):
            track.image = track_json['art_url']
        track.location = track_json['song_url']
        x.add_track(track)


    return x.toXml(), status.HTTP_200_OK


# ------- HTML REQUESTS -------
def playlist_request(id):
    payload = {'id': id}
    if not DEBUG_MODE:
        # Actual url
        url = TARGET_URL + PLAYLIST_EPT
    else:
    # Debug pre-kong url
        url = 'http://localhost:5200/' + PLAYLIST_EPT
    debugPrint(url)
    r = req.get(url, params=payload)
    debugPrint(r.url)
    debugPrint(r.json())
    return r

def tracks_request(song_url):
    payload = {'song_url': song_url}
    if not DEBUG_MODE:
        # Actual url
        url = TARGET_URL + TRACKS_EPT
    else:
    # Debug pre-kong url
        url = 'http://localhost:500/' + TRACKS_EPT
    debugPrint(url)
    r = req.get(url, params=payload)
    debugPrint(r.url)
    debugPrint(r.json())
    return r