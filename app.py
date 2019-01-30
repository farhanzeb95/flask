import os
from flask import Flask, jsonify, json, request, session, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_bcrypt import Bcrypt
from werkzeug import secure_filename
from AddUser import User, AddItem

UPLOAD_FOLDER = 'Item_Images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_DBNAME']= 'GDSD'
app.config['MONGO_URI']= 'mongodb://localhost:27017/new_user'

app.secret_key='secretkey'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/items/search', methods=["GET"])
def search():
    print(request)
    return jsonify([])

@app.route('/me', methods=["GET"])
def me():
    if 'email' in session:
        return redirect('/items/search', 302)
    

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

@app.route('/newitem', methods=['POST'])
def AddItem():
    users= mongo.db.items
    name= request.form['name']
    description= request.form['description']
    condition= request.form['condition']
    price= request.form['price']
    category= request.form['category']
    email= request.form['email']
    image= request.files['image']
    if 'image' not in request.files:
        return jsonify('no file uploaded')
        image= request.files['image']
    if image.filename== '':
        return jsonify('no file selected')
    if not allowed_file(image.filename):
        return jsonify('invalid')

    if image: 
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if 'email' in session:
        product_id= users.insert({
            'name': name,
            'description': description,
            'condition': condition,
            'price': price,
            'category': category,
            'email': email,
            'image': filename
            })
        return('Item Added to Database')
        
    else:
        return jsonify('You are not logged in'), 400
            
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return "You are Logged Out"
if __name__ == '__main__':
    app.debug = True
    app.run()    
