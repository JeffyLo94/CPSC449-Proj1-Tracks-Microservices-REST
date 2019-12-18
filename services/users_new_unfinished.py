import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import werkzeug

from flask_cassandra import CassandraCluster

#   -----   Initialization of the Flask API
app = flask_api.FlaskAPI(__name__)
#   -----   Reading the configfile using .env
app.config.from_envvar('APP_CONFIG')

scylla = CassandraCluster()

app.config['CASSANDRA_NODES'] = ['172.17.0.2']

#   -----   PugSQL module for getting queries from a folder
# queries = pugsql.module('queries/')
#   -----   Connect to the neccessary database
# queries.connect(app.config['DATABASE_URL'])

#   -----   This creates the init command functionality
#           for flask in order to compile the Database
#           using the sql script
@app.cli.command('init')
def init_db():
    with app.app_context():
        #   How do I even do this in noSQL?
        db = queries._engine.raw_connection()
        with app.open_resource('trackmeet.cql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def debugPrint(data):
    print(data, file=sys.stderr)
#   -----   This will be shown if the webpage is opened at
#           the host defined by flask. No front-end yet so
#           this is the place holder for it.
@app.route('/', methods=['GET'])
def home():
    return '''<h1>TrackMeet Users Archive</h1>
<p>A prototype API for User objects.</p>'''

#   -----   DEBUG only function ?
@app.route('/user/all', methods=['GET'])
def all_users():
    session = scylla.connect()
    session.set_keyspace("trackmeet")
    cql = "SELECT * FROM users"
    r = session.execute(cql)
    # all_users = queries.all_users()
    return str(r[0])

#   -----   DEBUG only function ?
@app.route('/user/<int:id>', methods=['GET','DELETE'])
def user_by_id(id):
    if request.method == 'GET':
        return user(id)
    elif request.method == 'DELETE':
        return del_user(id)

def user(id):
    session = scylla.connect()
    session.set_keyspace("trackmeet")
    cql = "SELECT * FROM users WHERE id = " + str(id)
    user = session.execute(cql)
    # user = queries.user_by_id(id = id)
    if user:
        return str(user)
    else:
        raise exceptions.NotFound()

#   -----   This will be used when deleting a user.
#           It is called from the /user path
def del_user(id):
    # id = data.get('id')

    debugPrint('attempting to delete id:')
    debugPrint(id)

    session = scylla.connect()
    session.set_keyspace("trackmeet")
    cql = "DELETE FROM users WHERE id = " + str(id)
    user = session.execute(cql)
    # rows_changed = queries.del_user_by_id(id=id)

    debugPrint('user: ')
    debugPrint(user)

    if(user == 1):
        debugPrint('inside rows_changed == 1 stmt')
        debugPrint(status.HTTP_200_OK)
        return {'message':'User deleted successfully!'}, status.HTTP_200_OK
    elif(user > 1): #   If multiple rows with same id, something's wrong
        return {'message': 'Conflict noticed upon deletion'},status.HTTP_409_CONFLICT
    else:
        raise exceptions.NotFound()

#   -----   This will be used to get the neccessary users or
#           create a new user using parameters
@app.route('/user',methods=['GET','POST','PUT'])
def users():
    if request.method == 'GET':
        return filter_users(request.args)
    elif request.method == 'POST':
        return create_user(request.data)
    elif request.method == 'PUT':
        return change_pass(request.args,request.data)



@app.route('/user/chpass/',methods=['PUT'])
def change_pass():
    data = request.data
    # id = data['id']
    userN = data['username']
    passW = data['password']
    debugPrint('passW: ')
    debugPrint(passW)

    password = werkzeug.generate_password_hash(str(passW))



    user = queries.change_pass(password = password,username = userN)
    debugPrint('user in change_pass: ')
    debugPrint(user)
    if(user == 1):
        return str(status.HTTP_200_OK)
    if(user > 1):
        return {'message': 'more than one item was affected'}, status.HTTP_409_CONFLICT
    else:
        raise exceptions.NotFound()


@app.route('/user/auth',methods=['POST'])
def Authenticate():
    data = request.data
    reqUsername = data['username']
    reqPassword = data['password']

    debugPrint('reqUsername: ')
    debugPrint(reqUsername)

    debugPrint('reqPassword: ')
    debugPrint(reqPassword)

    debugPrint('inside authenticate BEFORE getting password')
    password = queries.get_password_by_username(username = reqUsername)
    debugPrint('inside authenticate after getting password')

    debugPrint('password: ')
    debugPrint(password)

    # reqPassword = werkzeug.generate_password_hash(str(reqPassword))

    debugPrint('reqPassword after werkzeug: ')
    debugPrint(reqPassword)

    # werkzeug.check_password_hash(password,reqPassword)

    debugPrint('after checking outside if stmt')
    debugPrint(werkzeug.check_password_hash(password,str(reqPassword)))

    if not password:
        raise exceptions.NotFound()
    if(werkzeug.check_password_hash(password,str(reqPassword))):
        debugPrint('we got in!')
        debugPrint(str(status.HTTP_200_OK))
        return {'message':'Access granted!'}, status.HTTP_200_OK

    debugPrint('we did not get in!')
    debugPrint(str(status.HTTP_403_FORBIDDEN))
    return {'message':'Forbidden access'}, status.HTTP_403_FORBIDDEN

#       MAYBE for later
# @app.route('/user/<string:username>')
# def getIdByName():
#     pass

def get_by_name():
    pass

#   -----   Checks for validity and for redundancy
#           If neither than return the book and say OK
def create_user(user):
    # user = request.data
    required_fields = ['username','password','displayname','email']

    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user['password'] = werkzeug.generate_password_hash(user['password'])
        user['id'] = queries.create_user(**user)
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT

    debugPrint('this id of the newly created user: ')
    debugPrint(user['id'])
    debugPrint(user['password'])
    return user, status.HTTP_201_CREATED

#   -----   Filter users
def filter_users(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    displayname = query_parameters.get('displayname')
    email = query_parameters.get('email')
    url = query_parameters.get('url')   #   Optional

    query = "SELECT username, displayname, email, url FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if displayname:
        query += ' displayname=? AND'
        to_filter.append(displayname)
    if email:
        query += ' email=? AND'
        to_filter.append(email)
    if url:
        query += ' url=? AND'
        to_filter.append(url)
    # if url is None:
    #     to_filter.append(None)
    if not (id or username or displayname or email):
        raise exceptions.NotFound()

    query = query[:-4] +';'

    results = queries._engine.execute(query,to_filter).fetchall()
    return list(map(dict,results))


if __name__ == "__main__":
    app.run(debug=True)
