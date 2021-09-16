from flaskapp.models.show import Show
from flaskapp import app
from flask import render_template, redirect, request, session

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', shows = Show.get_all_shows_with_users())

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

@app.route('/show/<int:show_id>/edit')
def edit(show_id):
    data = {
        'id' : show_id
    }
    return render_template('edit.html', show = Show.get_one(data))

@app.route('/show/<int:show_id>/update', methods=['POST'])
def update_show(show_id):
    # data = {
    #     'id' : show_id,
    #     'title': request.form['title'],
    #     'description': request.form['description'],
    #     'release_date': request.form['release_date'],
    # }
    Show.update_show(request.form)
    return redirect('/dashboard')

@app.route('/show/<int:show_id>/delete')
def destroy(show_id):
    data = {
        'id': show_id
    }
    Show.destroy(data)
    return redirect('/dashboard')

@app.route('/show/<int:show_id>')
def show_page(show_id):
    data = {
        'id': show_id
    }
    return render_template('one_show.html', show=Show.get_one(data))
