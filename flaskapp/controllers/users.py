from flaskapp import app
from flask import render_template, redirect, session, request, flash
from flaskapp.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
    }
    valid = User.user_validator(data)
    if valid:
        hashed_pw = bcrypt.generate_password_hash(request.form['password'])
        data['hashed_pw'] = hashed_pw
        user = User.create_user(data)
        print(user)
        session['user_id'] = user
        print("Way to go! User Created!")
        return redirect('/dashboard')
    # user = User.create_user(data)
    # return redirect('/success')
    return redirect('/')

@app.route('/user/login', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password.')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password.')
        return redirect('/')
    session['user_id'] = user.id
    print("Successful login")
    return redirect('/dashboard')

# @app.route('/user/success')
# def success():
#     if 'user_id' not in session:
#         return redirect('/')
#     return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')