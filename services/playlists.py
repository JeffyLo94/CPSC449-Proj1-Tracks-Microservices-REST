import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import sys

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

def debugPrint(data):
    print(data, file=sys.stderr)

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


@app.route('/playlists/all', methods=['GET'])
def all_playlists():
    debugPrint('GETTING ALL Playlists')
    all_playlists = queries.all_playlists()
    pListArr = list(all_playlists)
    for p in pListArr:
        # debugPrint(p)
        id = p['id']
        try:
            urls = queries.all_urls_for_playlist(playlistID=id)
            p['urls'] = list(urls)
            # debugPrint(p)
        except Exception as e:
            return {'error': str(e)}, status.HTTP_409_CONFLICT
    debugPrint(pListArr)

    return pListArr, status.HTTP_200_OK

@app.route('/playlists/<string:user>', methods=['GET'])
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


@app.route('/playlists/<int:id>', methods=['DELETE'])
def delete_playlist_by_id(id):
    debugPrint(id)
    playlist = queries.playlist_by_id(id=id)
    if playlist:
        debugPrint('attempting delete urls')
        try:
            # Query for deletion is deleting from table, but throws an error,
            # so doing this stupid jank ass exception code to bypass
            queries.delete_playlist_urls_by_id(id=id)

            debugPrint('attempting delete playlist')
            queries.delete_playlist_by_id(id=id)
            return {'message': 'Playlist successfully deleted'}, status.HTTP_200_OK
        except Exception as e:
            debugPrint('PUGSQL is shit')
            debugPrint('attempting delete playlist')
            try:
                queries.delete_playlist_by_id(id=id)
                return {'message': 'Playlist successfully deleted'}, status.HTTP_200_OK
            except:
                return {'message': 'Playlist successfully deleted'}, status.HTTP_200_OK
        # except Exception as e:
            debugPrint(e)
            return {'error': str(e)}, status.HTTP_409_CONFLICT
    else:
        debugPrint('not found')
        raise exceptions.NotFound()

# @app.route('/playlists', methods=['DELETE'])
# def delete_by_id(id):
#     if not id:
#         return { 'message': 'Need id'}, status.HTTP_409_CONFLICT
#     else:
#         playlist = queries.playlist_by_id(id=id)
#         if playlist:
#             try:
#                 queries.delete_playlist_by_id(id=id)
#                 return { 'message': 'Playlist successfully deleted'}, status.HTTP_200_OK
#             except Exception as e:
#                 if (e == 'This result object does not return rows. It has been closed automatically.'):
#                     return {'message': 'Playlist successfully deleted'}, status.HTTP_200_OK
#                 else:
#                     debugPrint(e)
#                     return {'error': str(e)}, status.HTTP_409_CONFLICT
#         else:
#             raise exceptions.NotFound()

@app.route('/playlists', methods=['DELETE'])
def delete_all_playlist():
    try:
        queries.delete_all_playlist_urls()
    except Exception as e:
        try:
            query = "DELETE FROM playlists"
            results = queries._engine.execute(query)
            # delete_all_playlist = queries.delete_all_playlists()
            debugPrint('deleted all playlists')
            return { 'message': 'All playlists successfully deleted'}, status.HTTP_200_OK
        except Exception as e:
            if (e == 'This result object does not return rows. It has been closed automatically.'):
                debugPrint('')
                return {'message': 'All playlists successfully deleted'}, status.HTTP_200_OK
            else:
                debugPrint(e)
                return {'error': str(e)}, status.HTTP_409_CONFLICT


@app.route('/playlists', methods=['DELETE'])
def delete_playlist(playlist):
    required_fields = ['title', 'creator']

    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        delete_playlist(**playlist)
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
    required_fields = ['title', 'urls', 'creator', 'description']

    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        playlist['id'] = queries.create_playlist(**playlist)
        uList = playlist['urls']
        id = playlist['id']
        debugPrint(uList)
        debugPrint(type(uList))
        debugPrint(id)
        for i in range(len(uList)):
            debugPrint(uList[i])
            data = {
                'url': uList[i],
                'playlistID': id
            }
            queries.create_playlists_url_list(data)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return playlist, status.HTTP_201_CREATED

def filter_playlists(query_parameters):
    id = query_parameters.get('id')
    title = query_parameters.get('title')
    urls = query_parameters.get('urls')
    creator = query_parameters.get('creator')
    description = query_parameters.get('description')

    if not id and not title and not urls and not creator and not description:
        return all_playlists()


    debugPrint('ENTERED FILTER PLAYLISTS')
    debugPrint(id)

    query = "SELECT * FROM playlists WHERE"
    to_filter = {}

    if id:
        query += ' id=:id AND'
        to_filter.update({'id': id})
    if title:
        query += ' title=:title AND'
        to_filter.update({'title': title})
    if urls:
        query += ' urls=:urls AND'
        to_filter.update({'urls': urls})
    if creator:
        query += ' creator=:creator AND'
        to_filter.update({'creator':creator})
    if description:
        query += ' description=:desc AND'
        to_filter.update({'desc':description})
    if not (id or title or urls or creator or description):
        debugPrint('not found triggered')
        raise exceptions.NotFound()

    query = query[:-4] + ';'
    debugPrint(query)
    try:
        results = queries._engine.execute(query, to_filter).fetchall()
        debugPrint(results)
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT

    return list(map(dict, results))