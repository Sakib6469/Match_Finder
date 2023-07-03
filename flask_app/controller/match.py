from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.matches import Match
from flask_app.controller import user
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create/profile')
def profile():
    return render_template('profile.html')

@app.route('/new/profile/made', methods=['POST'])
def process():
    if 'user_id' not in session:
        return redirect('/')
    if not Match.validate(request.form):
        return redirect('/create/profile')

    form_data = {
        'user_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age'],
        'city': request.form['city'],
        'description': request.form['description'],
        'picture': request.form['picture']
    }
    Match.save(form_data)
    return redirect('/home/matches')



@app.route('/home/matches')
def matches():
    user_id = session.get('user_id')
    matches = Match.get_all()
    return render_template('home.html', user=User.get_all() , matches=matches)











