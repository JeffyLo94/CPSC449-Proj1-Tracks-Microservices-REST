import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import werkzeug

#   -----   Initialization of the Flask API
app = flask_api.FlaskAPI(__name__)
#   -----   Reading the configfile using .env
app.config.from_envvar('APP_CONFIG')

#   -----   PugSQL module for getting queries from a folder
queries = pugsql.module('queries/')
#   -----   Connect to the neccessary database
queries.connect(app.config['DATABASE_URL'])

#   -----   This creates the init command functionality
#           for flask in order to compile the Database
#           using the sql script
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('users.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#   -----   This will be shown if the webpage is opened at
#           the host defined by flask. No front-end yet so
#           this is the place holder for it.
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Music Archive</h1>
<p>A prototype API for distant browsing of music tracks you can't listen to.</p>'''

#   -----   DEBUG only function ?
@app.route('/user/all', methods=['GET'])
def all_users():
    all_users = queries.all_users()
    return list(all_users)

#   -----   DEBUG only function ?
@app.route('/user/<int:id>')
def user(id):
    user = queries.user_by_id(id = id)
    if user:
        return user
    else:
        raise exceptions.NotFound()

#   -----   This will be used to get the neccessary users or
#           create a new user using parameters
@app.route('/user',methods=['GET','POST','DELETE'])
def users():
    if request.method == 'GET':
        return filter_users(request.args)
    elif request.method == 'POST':
        return create_user(request.data)
    elif request.method == 'DELETE':
        return del_user(request.args)

#   -----   This will be used when deleting a user.
#           It is called from the /user path
def del_user(data):
    id = data.get('id')
    rows_changed = queries.del_user_by_id(id=id)
    if(rows_changed == 1):
        return status.HTTP_200_OK
    elif(rows_changed > 1): #   If multiple rows with same id, something's wrong
        return status.HTTP_409_CONFLICT
    else:
        raise exceptions.NotFound()

@app.route('/user/chpass',methods=['PUT'])
def change_pass():
    # info = request.data
    id = request.data.get('id')
    password = werkzeug.generate_password_hash(request.data.get('password'))
    user = queries.change_pass(password = password,id = id)
    if(user):
        return status.HTTP_200_OK
    else:
        raise exceptions.NotFound()


@app.route('/user/auth',methods=['GET'])
def Authenticate():
    reqUsername = request.data.get('username')
    reqPassword = request.data.get('password')

    password = queries.get_password_by_username(username = reqUsername)
    if not password:
        raise exceptions.NotFound()
    if(werkzeug.check_password_hash(reqPassword,password)):
        return status.HTTP_200_OK
    else:
        return status.HTTP_403_FORBIDDEN

#       MAYBE for later
# @app.route('/user/<string:username>')
# def getIdByName():
#     pass

#   -----   Checks for validity and for redundancy
#           If neither than return the book and say OK
def create_user(user):
    user = request.data
    required_fields = ['username','password','displayname','email']

    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user['password'] = werkzeug.generate_password_hash(user['password'])
        user['id'] = queries.create_user(**user)
    except Exception as e:
        return {'error': str(e)}, status.HTTP_409_CONFLICT

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
    if not (id or username or displayname or email):
        raise exceptions.NotFound()

    query = query[:-4] +';'

    results = queries._engine.execute(query,to_filter).fetchall()
    return list(map(dict,results))


if __name__ == "__main__":
    app.run(debug=True)
