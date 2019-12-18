import flask_api
from flask_api import status
import pugsql
import requests as req
import sys
from services.modules import xspf
from pymemcache.client import base
from pymemcache import fallback


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
DEBUG_MODE = False
CACHE_XML = False

old_cache = base.Client(('localhost', 11211), ignore_exc=True)
new_cache = base.Client(('localhost', 11212))
client = fallback.FallbackClient((new_cache, old_cache))
MEMCACHE_EXPIRE_SECONDS = 60



def debugPrint(data):
    if DEBUG_MODE:
        print(data, file=sys.stderr)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>XSPF MICROSERVICE</h1>
    <p> An API for generating XPSF playlists'''

@app.route('/playlist/<int:id>.xspf', methods=['GET'])
def generate_xspf_by_id(id):
    debugPrint(id)

    # Don't forget to run `memcached' before running this code
    if CACHE_XML:
        result = client.get(id)
    else:
        result = None

    if result is None:
        # The cache is empty, need to get the value
        # from the canonical source:
        jsonlist = playlist_request(id)
        x = xspf.Xspf()

        try:
            if len(jsonlist) > 0:
                json = jsonlist[0]
                x.title = json['title']
                x.identifier = str(json['id'])
                x.creator = json['creator']
                x.info = json['description']
                for t_url in json['urls']:
                    debugPrint(t_url)
                    track_jsonlist = tracks_request(t_url['url'])
                    debugPrint('track')
                    debugPrint(track_jsonlist)
                    track_json = track_jsonlist[0]
                    debugPrint(track_json)
                    track = xspf.Track()
                    track.title = track_json['title']
                    track.identifier = track_json['guid']
                    track.album = track_json['album']
                    track.duration = str(track_json['songLength'])
                    track.creator = track_json['artist']
                    if (track_json['art_url']):
                        track.image = track_json['art_url']
                    track.location = track_json['song_url']
                    debugPrint('adding track')
                    x.add_track(track)
        except Exception as e:
            debugPrint(e)
            return {'error': str(e)}, status.HTTP_409_CONFLICT

        try:
            debugPrint(x.toXml())
        except Exception as e:
            debugPrint(e)
            return {'error': str(e)}, status.HTTP_409_CONFLICT

        result = x.toXml()
        if CACHE_XML:
            # Cache the result for next time:
            client.set(id, result, expire=MEMCACHE_EXPIRE_SECONDS)

    # Whether we needed to update the cache or not,
    # at this point you can work with the data
    # stored in the `result` variable:
    print(result)
    return result, status.HTTP_200_OK


# ------- HTML REQUESTS -------
def playlist_request(id):
    cache_key = 'playlist_' + str(id)
    result = client.get(cache_key)
    if result is None:
        payload = {'id': id}

        if not DEBUG_MODE:
            # Actual url
            url = TARGET_URL + PLAYLIST_EPT +'/' + PLAYLIST_EPT + str(id)
        else:
            # Debug pre-kong url
            url = 'http://localhost:5200/' + PLAYLIST_EPT
        debugPrint(url)
        r = req.get(url, params=payload)
        debugPrint(r.url)
        debugPrint(r.json())
        result = r.json()
        client.set(cache_key, result, expire=MEMCACHE_EXPIRE_SECONDS)
    return result


def tracks_request(song_url):
    cache_key = 'tracks_' + str(song_url)
    result = client.get(cache_key)

    if result is None:
        payload = {'song_url': song_url}
        if not DEBUG_MODE:
            # Actual url
            url = TARGET_URL + TRACKS_EPT
        else:
        # Debug pre-kong url
            url = 'http://localhost:5100/' + TRACKS_EPT
        debugPrint(url)
        r = req.get(url, params=payload)
        debugPrint(r.url)
        debugPrint(r.json())
        result = r.json()
        client.set(cache_key, result, expire=MEMCACHE_EXPIRE_SECONDS)
    return result
