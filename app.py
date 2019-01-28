from flask import Flask, jsonify, json, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_bcrypt import Bcrypt
from AddUser import User

app = Flask(__name__)
app.debug = True
app.config['MONGO_DBNAME']= 'GDSD'
app.config['MONGO_URI']= 'mongodb://localhost:27017/new_user'

app.secret_key='secretkey'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/items/search', methods=["GET"])
def search():
    print(request)
    return jsonify([])

@app.route('/me', methods=["GET"])
def me():
    return jsonify([])

@app.route('/user/signup', methods=["POST"])
def register():
    user = User()
    error = user.validate(request.get_json())
    print(error)
    if error:
        return jsonify('error'), 400
    else:
        users = mongo.db.users
        username = request.get_json()['username']
        eemail = request.get_json()['email']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        created = datetime.utcnow()
        
        if users.find_one({ 'email' : eemail}):
            return jsonify("user already exists"), 400
        else:
            user_id = users.insert({
                'username': username,
                'email': eemail,
                'password': password,
                'created': created
                })

        new_user = users.find_one({'_id': user_id})

        result = {'email': new_user['email'] +  'Registered'}
        return jsonify({'result': result}), 201

@app.route('/user/login', methods=['POST'])
def login():
    users = mongo.db.users
    
    # print(request.get_json()['email'])
    
    email = request.get_json()['email']
    password = request.get_json()['password']

    userss = users.find({ 'email' : email})
    for user in userss:
        if user and bcrypt.check_password_hash(user['password'], password):
            session['email']=user['email']
            return jsonify("Login Successful"), 200
    return jsonify("Invalid Email or Password"), 501

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return "You are Logged Out"
if __name__ == '__main__':
    app.debug = True
    app.run()    
