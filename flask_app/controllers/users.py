from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/') # default route
def index():
    return render_template('home.html')

@app.route('/create_user', methods=['POST'])
def register():
    if not User.validate_create(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.create_user(data)
    session['user_id'] = user_id
    return redirect('/main')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid email/password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/main')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
