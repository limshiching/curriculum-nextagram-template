from flask_wtf.csrf import CSRFProtect
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_manager, current_user
from instagram_web.util.google_helpers import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/sessions')
                            

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@sessions_blueprint.route('/create', methods= ['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.get_or_none(User.email == email)
    if not user:
        flash('Email not valid', 'warning')
        return redirect(url_for('sessions.new'))

    if not check_password_hash(user.password, password):
        flash('Password invalid', 'danger')
        return redirect(url_for('sessions.new'))

    login_user(user)
    session["username"] = "username"
    flash('Welcome, successfully signed in.')
    return redirect(url_for('users.show', id=user.id))

@sessions_blueprint.route('new/google', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('authorize/google', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()
    response = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo')
    email = response.json()['email']

    user = User.get_or_none(User.email == email)

    if not user:
        flash('Failed')
        return render_template('new.html')

    login_user(user)
    # Flash message = "Welcome back user"
    return redirect(url_for('users.show', id=user.id))

@sessions_blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out successfully')
    return redirect(url_for('home'))
        
