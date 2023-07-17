from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.matches import Match
from flask_app.models.message import Message
from flask_app.controller import match
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import os
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
        # matches = Match.get_all()
        session['user_id'] = user_id
        print(user_id)
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
    id = session.get('id')
    return render_template('home.html',user=User.get_by_id({'id': id}))



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




#messages


@app.route('/message/users')
def message():
    loged_in_user = session['user_id']
    users = User.get_all_except(loged_in_user)
    return render_template('messages.html', users=users)




@app.route('/message/users/text/<int:recipient_id>',methods=['GET','POST'])
def text_users(recipient_id):
    message = Message.get_users_messages('data')
    user_id_recipient = recipient_id
    return render_template('text_user.html',message=message,user_id_recipient=user_id_recipient)

@app.route('/message/users/text/send', methods=['POST'])
def send_message():
    data = {
        "text": request.form['text'],
        "user_id_sender": request.form['user_id_sender'],
        "user_id_recipient": request.form['user_id_recipient']
    }
    message = Message.save_message(data)
    if message:
        flash("Message Sent!!!")
    return redirect(f'/message/users/text/{{')
