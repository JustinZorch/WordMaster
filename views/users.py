from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from common.database import Database
from models.user.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/signup', methods=['POST', 'GET'])
def register_user():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form["name"]

        if email == "" or password == "" or name == "":
            flash("Please don't leave any fields blank.", "danger")
            return redirect(url_for('.register_user'))
        else:

            if User.is_email_used(email):
                User.register_user(email, password, name)
                session['email'] = email
                return redirect(url_for('.welcome'))
            else:
                flash('The e-mail you used to register already exists', 'danger')

    return render_template('users/signup.html')


@user_blueprint.route('/welcome', methods=['POST', 'GET'])
def welcome():

    user = Database.find_one("users", {"email": session['email']})

    return render_template('welcome.html', name=user["name"])


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "" or password == "":
            flash("Please enter your email and password", "danger")
            return redirect(url_for('.login_user'))

        else:

            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.welcome'))
            else:
                flash("Your password was incorrect.", "danger")

    return render_template('users/login.html')

@user_blueprint.route('/logout')
def log_out():
    session['email'] = None
    return redirect(url_for('.login_user'))


