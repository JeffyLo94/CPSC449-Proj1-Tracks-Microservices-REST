import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

#   -----   Initialization of the Flask API
app = flask_api.FlaskAPI(__name__)
#   -----   Reading the configfile using .env
app.config.from_envvar('APP_CONFIG')

#   -----   PugSQL module for getting queries from a folder
queries = pugsql.module('queries/')
#   -----   Connect to the neccessary database
queries.connect(app.config['DATABASE_URL'])

def debugPrint(data):
    print(data, file=sys.stderr)


#   -----   This creates the init command functionality
#           for flask in order to compile the Database
#           using the sql script
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('descriptions.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#   -----   This will be shown if the webpage is opened at
#           the host defined by flask. No front-end yet so
#           this is the place holder for it.
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Descriptions Archive</h1>
<p>A prototype API for descriptions of tracks.</p>'''

#   -----   DEBUG only function ?
@app.route('/desc/all', methods=['GET'])
def all_desc():
    all_desc = queries.all_descriptions()
    return list(all_desc)

#   -----   DEBUG only function ?
@app.route('/desc/<int:id>', methods=['GET'])
def desc(id):
    desc = queries.desc_by_id(id = id)
    if desc:
        return desc
    else:
        raise exceptions.NotFound()

@app.route('/desc/<int:id>', methods=['DELETE'])
def delete_desc_by_id(id):
    desc = queries.desc_by_id(id = id)
    if desc:
        debugPrint('attempting to delete id:')
        debugPrint(id)
        query = "DELETE FROM descriptions WHERE id=?"
        params = [id]
        try:
            result = queries._engine.execute(query,params)
            debugPrint('deleted desc of id' + str(id))
            # debugPrint(list(map(dict,result)))
            return {'message': 'DELETED description'}, status.HTTP_202_ACCEPTED
        except Exception as e:
            return {'error': str(e)}, status.HTTP_409_CONFLICT


#   -----   This will be used to get the neccessary users or
#           create a new user using parameters
@app.route('/desc',methods=['GET','POST'])
def descriptions():
    if request.method == 'GET':
        return filter_desc(request.args)
    elif request.method == 'POST':
        return create_desc(request.data)


def create_desc(desc):
    desc = request.data
    required_fields = ['username','trackurl','description']

    if not all([field in desc for field in required_fields]):
        raise exceptions.ParseError()
    try:
        desc['id'] = queries.create_desc(**desc)
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT

    return desc, status.HTTP_201_CREATED

def filter_desc(query_parameters):
    id = query_parameters.get('id')
    user = query_parameters.get('username')
    trackurl = query_parameters.get('trackurl')
    description = query_parameters.get('description')

    query = "SELECT * FROM descriptions WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if user:
        query += ' username=? AND'
        to_filter.append(user)
    if trackurl:
        query += ' trackurl=? AND'
        to_filter.append(trackurl)
    if description:
        query += ' description=? AND'
        to_filter.append(description)
    if not (id or user or trackurl or description):
        raise exceptions.NotFound()

    query = query[:-4] + ';'
    debugPrint(query)
    debugPrint(to_filter)
    try:
        results = queries._engine.execute(query,to_filter).fetchall()
        debugPrint(map(dict,results))
    except Exception as e:
        debugPrint(e)
        return {'error': str(e)}, status.HTTP_409_CONFLICT
    return list(map(dict,results))

if __name__ == "__main__":
    app.run(debug=True)
