from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.matches import Match
from flask_app.controller import user
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/home/matches')
def matches():
    user_id = session.get('user_id')
    # matches = Match.get_all()
    return render_template('home.html', user=User.get_all() , matches=matches)



#Destroy
@app.route('/destroy/matches/<int:id>')
def delete(id):
    Match.destroy({'id': id})
    return redirect('/home/matches')
