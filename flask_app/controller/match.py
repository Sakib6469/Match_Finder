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
    user_id = session.get('users_id')
    matches = Match.get_all()
    user = User.get_by_id('users_id')
    return render_template('home.html', user=user, matches=matches)












#Deleate
@app.route('/destroy/matches/<int:id>')
def delete(id):
    Match.destroy({'id': id})
    return redirect('/home/matches')

#view matches
@app.route('/view/matches/<int:id>')
def view_matches(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('show.html',match=Match.get_by_id({'id': id}),user=user)





@app.route('/update/matches/<int:id>')
def update(id):
    matches = Match.get_one({'id':id})
    return render_template('update.html',matches=matches)




@app.route('/matches/edit/<int:id>', methods=['GET', 'POST'])
def process_edit_matches(id):
    if request.method == 'POST':
        # Process the form submission
        if 'user_id' not in session:
            return redirect('/')
    
        form_data = request.form.to_dict()
    
        if not Match.validate(form_data):
            return redirect(f'/matches/edit/{id}')
    
        form_data['id'] = id
        Match.update(form_data)
        return redirect('/home/matches')
    else:
        # Handle GET request (rendering the form)
        matches = Match.get_one({'id': id})
        return render_template('update.html', matches=matches)