from flaskapp.models.show import Show
from flaskapp import app
from flask import render_template, redirect, request, session

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', shows = Show.get_all_shows())

@app.route('/show/create', methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/')
    valid = Show.show_validator(request.form)
    if valid:
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'release_date': request.form['release_date'],
            'users_id': session['user_id']
        }
        show = Show.create_show(data)
        return redirect (f'/show/{show}')
    return redirect('/show/add_show')

@app.route('/show/add_show')
def add_show_form():
    return render_template('new_show.html')
