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
        with app.open_resource('playlists.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>PLAYLIST MICROSERVICE</h1>
<p>A prototype API for our playlists microservice.</p>'''


@app.route('/playlists', methods=['GET'])
def all_playlists():
    all_playlists = queries.all_playlists()
    return list(all_playlists), status.HTTP_200_OK

@app.route('/playlists', methods=['GET'])
def playlist_by_user(query_parameters):
    playlist_by_user = queries.playlist_by_user()
    return list(playlist_by_user), status.HTTP_200_OK


@app.route('/playlists/<int:id>', methods=['GET'])
def playlist_by_id(id):
    playlist = queries.playlist_by_id(id=id)
    if playlist:
        return playlist, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()

@app.route('/playlists', methods=['DELETE'])
def delete_by_id(id):
    if not id:
        return { 'message': 'Need id'}, status.HTTP_409_CONFLICT
    else:
        queries.delete_playlist(id=id)
        return { 'message': 'Playlist successfully deleted'}, status.HTTP_200_OK

@app.route('/playlists', methods=['DELETE'])
def delete_all_playlist():
    delete_all_playlist = queries.delete_all_playlist()

@app.route('playlists', methods=['DELETE'])
def delete_playlist(playlist):
    required_fields = ['title', 'creator']

    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        queries.delete_playlist(**playlist)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

@app.route('/playlists', methods=['GET', 'POST', 'DELETE'])
def playlists():
    if request.method == 'GET':
        return filter_playlists(request.args)
    elif request.method == 'POST':
        return create_playlist(request.data)
    elif request.method == 'DELETE':
        return delete_playlist(request.data)

@app.route('/playlists', methods=['POST'])
def create_playlist(playlist):
    required_fields = ['title', 'urls', 'creator']

    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        playlist['id'] = queries.create_playlist(**playlist)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return playlist, status.HTTP_201_CREATED

def filter_playlists(query_parameters):
    id = query_parameters.get('id')
    title = query_parameters.get('title')
    urls = query_parameters.get('urls')
    creator = query_parameters.get('creator')
    description = query_parameters.get('description')

    query = "SELECT * FROM playlists WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if urls:
        query += ' urls=? AND'
        to_filter.append(urls)
    if creator:
        query += ' creator=? AND'
        to_filter.append(creator)
    if description:
        query += ' description=? AND'
        to_filter.append(description)
    if not (id or title or urls or creator or description):
        raise exceptions.NotFound()

    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))