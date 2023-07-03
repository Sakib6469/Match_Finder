from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.matches import Match
from flask_app.controller import match
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Nav Bar
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
    # Check if the 'profile_pic' file exists in the request
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
        matches = Match.get_all()
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
    user_id = session.get('user_id')
    user = User.get_all()
    return render_template('home.html', user=user)



@app.route('/view/user/info/<int:id>')
def view_user_info(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id': id})
    if not user:
        flash("User not found.")
        return redirect('/home/matches')
    return render_template('show.html',user=User.get_user_by_id({'id': id}))




@app.route('/destroy/users/<int:id>')
def delete_user(id):
    User.destroy({'id': id})
    return redirect('/home/matches')