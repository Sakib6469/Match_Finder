from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.matches import Match
from flask_app.controller import match
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/create')

#Creating a acount
@app.route('/create')
def create():
    return render_template('greet.html')

@app.route('/register')
def display_form():
    return render_template('index.html')



@app.route('/register/user', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)

    if is_valid:
        if request.form['password'] == '':
            flash("Password is required.")
            return redirect('/create')

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
            "age": request.form['age'],
        }
        user_id = User.save(data)
        matches = Match.get_all()
        session['user_id'] = user_id
        print(user_id)
        return redirect('/home/matches')
    else:
        return redirect('/')

#Loging in
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
    user_id = session.get('user_id')
    user = User.get_all()
    return render_template('home.html', user=user)

@app.route('/destroy/users/<int:id>')
def delete_user(id):
    User.destroy({'id': id})
    return redirect('/home/matches')