import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import sqlite3
import uuid


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))

queries1 = pugsql.module('queries/track1/')
queries1.connect(app.config['DATABASE_URL_1'].format(stuff=sqlite3.PARSE_DECLTYPES))

queries2 = pugsql.module('queries/track2/')
queries2.connect(app.config['DATABASE_URL_2'].format(stuff=sqlite3.PARSE_DECLTYPES))

queries3 = pugsql.module('queries/track3/')
queries3.connect(app.config['DATABASE_URL_3'].format(stuff=sqlite3.PARSE_DECLTYPES))

def debugPrint(data):
    print(data, file=sys.stderr)

@app.cli.command('init')
def init_db():
    with app.app_context():
        db1 = queries1._engine.raw_connection()
        #db.create_all()
        with app.open_resource('track1.sql', mode='r') as f1:
            db1.cursor().executescript(f1.read())
        db1.commit()

        db2 = queries2._engine.raw_connection()
        with app.open_resource('track2.sql', mode='r') as f2:
            db2.cursor().executescript(f2.read())
        db2.commit()

        db3 = queries3._engine.raw_connection()
        with app.open_resource('track3.sql', mode='r') as f3:
            db3.cursor().executescript(f3.read())
        db3.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>TRACK MICROSERVICE</h1>
<p>A prototype API for our tracks microservice.</p>'''

#return ALL tracks
@app.route('/tracks/all', methods=['GET'])
def all_tracks():
    all_tracks1 = queries1.all_tracks()
    all_tracks2 = queries2.all_tracks()
    all_tracks3 = queries3.all_tracks()
    all_tracks = list(all_tracks1) + list(all_tracks2) + list(all_tracks3)

    return list(all_tracks)

#get track by id
@app.route('/tracks/<uuid:id>', methods=['GET'])
def track_by_id(id):
    #get the shardkey of id and find in respective database
    shardKey = id % 3

    if shardKey == 0:
        track = queries1.track_by_id(id=id)
    elif shardKey == 1:
        track = queries2.track_by_id(id=id)
    elif shardKey == 2:
        track = queries3.track_by_id(id=id)
    else:
        raise exceptions.NotFound()
    return track

@app.route('/tracks', methods=['GET', 'POST', 'PUT'])
def tracks():
    if request.method == 'GET':
        return filter_tracks(request.args)
    elif request.method == 'POST':
        return create_track(request.data)
    elif request.method == 'PUT':
        return edit_track(request.data)
    # elif request.method == 'DELETE':
    #     return delete_track(request.data)

@app.route('/tracks', methods=['PUT'])
def edit_track(query_parameters):
    title = query_parameters.get('title')
    album = query_parameters.get('album')
    artist = query_parameters.get('artist')
    songLength = query_parameters.get('songLength')
    song_url = query_parameters.get('song_url')
    art_url = query_parameters.get('art_url')

    query = "SELECT * FROM tracks WHERE"
    to_edit = []

    if title:
        query += ' title=? AND'
        to_edit.append(title)
    if album:
        query += ' album=? AND'
        to_edit.append(album)
    if artist:
        query += ' artist=? AND'
        to_edit.append(artist)
    if songLength:
        query += ' songLength=? AND'
        to_edit.append(songLength)
    if song_url:
        query += ' song_url=? AND'
        to_edit.append(song_url)
    if art_url:
        query += ' art_url=? AND'
        to_edit.append(art_url)
    if not (id or title or album or artist or songLength or song_url):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    edit1 = queries1._engine.execute(query, to_edit).fetchall()
    edit2 = queries2._engine.execute(query, to_edit).fetchall()
    edit3 = queries3._engine.execute(query, to_edit).fetchall()

    return list(map(dict, edit1)) + list(map(dict, edit2)) + list(map(dict, edit3))


#delete track by id
@app.route('/tracks/<uuid:id>', methods=['DELETE'])
def delete_by_id(id):
    if not id:
        return { 'message': 'Need id'}, status.HTTP_409_CONFLICT
    shardKey = id % 3

    try:
        if shardKey == 0:
            queries1.delete_by_id(id=id)
        elif shardKey == 1:
            queries2.delete_by_id(id=id)
        elif shardKey == 2:
            queries3.delete_by_id(id=id)
        return { 'message': 'Track successfully deleted'}, status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT


# def delete_track(track):
#     required_fields = ['title', 'album', 'artist', 'song_url']
#
#     if not all([field in track for field in required_fields]):
#         raise exceptions.ParseError()
#     try:
#         queries.delete_track(**track)
#         return { 'message': 'Track successfully deleted'}, status.HTTP_200_OK
#     except Exception as e:
#         return { 'error': str(e) }, status.HTTP_409_CONFLICT

#delete ALL tracks
@app.route('/tracks/all', methods=['DELETE'])
def delete_all_tracks():
    queries1.delete_all_tracks()
    queries2.delete_all_tracks()
    queries3.delete_all_tracks()



def create_track(track):
    track = request.data
    required_fields = ['title', 'album', 'artist', 'songLength', 'song_url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        uniqueID = uuid.uuid4()
        shardKey = uniqueID % 3

        if shardKey == 0:
            track['id'] = uniqueID
            queries1.create_track(**track)
        elif shardKey == 1:
            track['id'] = uniqueID
            queries2.create_track(**track)
        elif shardKey == 2:
            track['id'] = uniqueID
            queries3.create_track(**track)
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
    if art_url:
        query += ' art_url=? AND'
        to_filter.append(art_url)
    if not (id or title or album or artist or songLength or song_url):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    results1 = queries1._engine.execute(query, to_filter).fetchall()
    results2 = queries2._engine.execute(query, to_filter).fetchall()
    results3 = queries3._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results1)) + list(map(dict, results2)) + list(map(dict, results3))
