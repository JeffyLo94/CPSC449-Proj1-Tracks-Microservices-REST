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


@app.route('/api/v1/resources/playlists/all', methods=['GET'])
def all_playlists():
    all_playlists = queries.all_playlists()
    return list(all_playlists)


@app.route('/api/v1/resources/playlists/<int:id>', methods=['GET'])
def playlist(id):
    playlist = queries.playlist_by_id(id=id)
    if playlist:
        return playlist
    else:
        raise exceptions.NotFound()


@app.route('/api/v1/resources/playlists', methods=['GET', 'POST'])
def playlists():
    if request.method == 'GET':
        return filter_playlists(request.args)
    elif request.method == 'POST':
        return create_playlist(request.data)


def create_playlist(playlist):
    required_fields = ['title', 'urls', 'user', 'description']

    if not all([field in track for field in required_fields]):
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
 	user = query_parameters.get('user')
 	description = query_parameters.get('description')

 	query = "SELECT * FROM tracks WHERE"
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
 	if user:
 		query += ' user=? AND'
 		to_filter.append(user)
 	if description:
 		query += ' description=? AND'
 		to_filter.append(description)
 	if not (id or title or urls or user or description):
 		raise exceptions.NotFound()

 	query = query[:-5] + ';'

 	results = queries._engine.execute(query, to_filter).fetchall()

 	return list(map(dict, results))















