from flask import flash, url_for, render_template, request, redirect, session

from flask_app.controllers.users import render_user_page

from flask_app import app
from flask_app.models.user import User
from flask_app.models.hub import Hub
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def homePage():
    pageName = "Front Page"
    print("User navigated to: " + pageName)
    return render_template("frontPage.html", pageName = pageName)

@app.route('/user/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "username":request.form['username'],
        "first_name":request.form['first_name'],  
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password_hash":pw_hash
    }
    user_id = User.save_user_to_db(data)
    session['user_id'] = user_id
    return redirect('/signup')

@app.route('/hub/create', methods=['POST'])
def create_hub():
    if not Hub.validate_hub(request.form):
        return redirect('/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "hub_name":request.form['hub_name'],
        "hub_email":request.form['hub_email'],
        "hub_location":request.form['hub_location'],  
        "hub_description":request.form['hub_description'],
        "password_hash":pw_hash
    }
    hub_id = Hub.save_hub_to_db(data)
    session['user_id'] = hub_id
    return redirect('/signup')

@app.route('/login', methods=['POST'])
def process_login():
    data = {
        'username':request.form['username']
    }
    user_in_db = User.get_by_username(data)
    if user_in_db == False:
        flash("No user with that username")
        return redirect('/signup')
    acceptable_id = User.validate_login(request.form, data)
    if acceptable_id == False:
        flash("invalid login credentials.")
        return redirect('/signup')
    # if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
    #     # if we get False after checking the password
    #     flash("Invalid login credentials.")
    #     return redirect('/signup')
    # if the passwords matched
    session['user_id'] = acceptable_id
    return redirect(url_for('render_user_page', user_id=acceptable_id))

@app.route('/signup')
def signup_form():
    pageName = "Sign up or sign in"
    return render_template('signUp.html', pageName = pageName)

@app.route('/hub/signup')
def signup_form_hub():
    pageName = "Hub sign up or sign in"
    return render_template('Hub/hubSignUp.html', pageName = pageName)

@app.route("/logout")
def log_out():
    session.clear()
    return redirect("/signup")

@app.route("/denied")
def denied_template():
    pageName = "Access Denied"
    return render_template('acessDenied.html', pageName = pageName)