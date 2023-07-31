from flask import render_template, request, redirect,session,url_for
from flask_app.models.users import User
from flask_app.models.matches import Match
from flask_app.models.messages import Message
from flask_app.controller import match
from flask_app.controller import message
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import session
import os
import googlemaps

API_KEY = 'AIzaSyCRNVWxNddzYlo0WBybnzau6Kd5L920Iw0'
map_client = googlemaps.Client(API_KEY)

# map_client.geocode()

UPLOAD_FOLDER = 'flask_app/static/uploaded_images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}




#Nav Bar Greeting Page
@app.route('/')
def index():
    return redirect('/greet')


@app.route('/greet')
def create():
    return render_template('greet.html')

@app.route('/carrer')
def carrer():
    return render_template('careers.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/info')
def info():
    return render_template('info.html')



#register
@app.route('/register')
def display_form():
    return render_template('register.html')

@app.route('/register/user', methods=['POST'])
def register():
    if 'profile_pic' not in request.files:
        flash("Profile picture is required.")
        return redirect('/register')

    profile_pic = request.files['profile_pic']

    is_valid = User.validate_user(request.form)

    if is_valid:
        if request.form['password'] == '':
            flash("Password is required.")
            return redirect('/register')

        # Check if the email is already registered
        existing_user = User.get_user_by_email({'email': request.form['email']})
        if existing_user:
            flash("Email already exists. Please choose a different email.")
            return redirect('/register')

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "location": request.form['location'],
            "email": request.form['email'],
            "password": pw_hash,
            "birthday": request.form['birthday'],
            "profile_pic": request.files['profile_pic']
        }
        
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/home')
    else:
        return redirect('/register')




#Login
@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/login/user',methods=['POST'])
def user_login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/home/matches')


#Home page


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    id = session.get('id')
    users = User.get_all_except('user_id')
    return render_template('home.html', users=users)



#Users CRUD
@app.route('/view/user/info/')
def view_user_info():
    id = session.get('user_id') 
    user = User.get_by_id({'id': id})
    return render_template('show.html', user=user)



@app.route('/destroy/users/<int:id>')
def delete_user(id):
    User.destroy({'id': id})
    return redirect('/')


@app.route('/edit/user/info', methods=['GET', 'POST'])
def edit_user_info():
    id = session.get('user_id')
    if request.method == 'POST':
        data = {
            "id": id,
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "location": request.form.get('location'),
            "email": request.form.get('email'),
            "profile_pic": request.files.get('profile_pic')
        }

        is_valid = User.edit_user(data)

        if is_valid:
            user = User.update(data)
            flash("User information updated successfully.")
            return redirect('/view/user/info/')
        else:
            return redirect('/edit/user/info')
    else:
        user = User.get_by_id({'id': id})
        return render_template('Edit_User.html', user=user)




#display imgs

# @app.config[''] == UPLOAD_FOLDER
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    
# @app.route('/ltg/submit', methods=['POST'])
# def create_ltg():
#     # Your other code...
#     if 'image' not in request.files:
#         flash('No file part')
#         return redirect('/ltg/form')
#     image = request.files['image']
#     print(image)
#     if image.filename == '':
#         flash('No selected file')
#         return redirect('/ltg/form')
#     if image and allowed_file(image.filename):
#         filename = secure_filename(image.filename)
#         print("Filename: ", filename)
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))