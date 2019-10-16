import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        db.create_all()
        with app.open_resource('tracks.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>TRACK MICROSERVICE</h1>
<p>A prototype API for our tracks microservice.</p>'''


@app.route('/tracks', methods=['GET'])
def all_tracks():
    all_tracks = queries.all_tracks()
    return list(all_tracks)

@app.route('/tracks/<int:id>', methods=['GET'])
def track_by_id(id):
    track = queries.track_by_id(id=id)
    if track:
        return track, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()


@app.route('/tracks', methods=['GET', 'POST', 'DELETE'])
def tracks():
    if request.method == 'GET':
        return filter_tracks(request.args)
    elif request.method == 'POST':
        return create_track(request.data)
    elif request.method == 'DELETE':
        return delete_track(request.data)


@app.route('/tracks', methods=['DELETE'])
def delete_track(id):
    if not id:
        return { 'message': 'Need id'}, status.HTTP_409_CONFLICT
    else:
        queries.delete_track(id=id)
        return { 'message': 'Track successfully deleted'}, status.HTTP_200_OK

@app.route('/tracks', methods=['POST'])
def create_track(track):
    required_fields = ['title', 'album', 'artist', 'songLength', 'song_url', 'art_url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track['id'] = queries.create_track(**track)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return track, status.HTTP_201_CREATED
    

def filter_tracks(query_parameters):
    id = query_parameters.get('id')
    title = query_parameters.get('title')
    album = query_parameters.get('album')
    artist = query_parameters.get('artist')
    songLength = query_parameters.get('songLength')
    song_url = query_parameters.get('song_url')
    art_url = query_parameters.get('art_url')

    query = "SELECT * FROM tracks WHERE"
    to_filter = []


    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if album:
        query += ' album=? AND'
        to_filter.append(album)
    if artist:
        query += ' artist=? AND'
        to_filter.append(artist)
    if songLength:
        query += ' songLength=? AND'
        to_filter.append(songLength)
    if song_url:
        query += ' song_url=? AND'
        to_filter.append(song_url)
    if art_urlt:
        query += ' art_url=? AND'
        to_filter.append(art_url)
    if not (id or title or album or artist or songLength or song_url or art_url):
        raise exceptions.NotFound()

    query = query[:-7] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))