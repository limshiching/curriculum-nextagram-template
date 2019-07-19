from flask_wtf.csrf import CSRFProtect
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape
from models import *
from werkzeug.security import generate_password_hash
import os


app = Flask(__name__)

# app.secret_key = os.getenv('SECRET_KEY')
# csrf = CSRFProtect(app)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')
                            

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/user/create', methods=['POST'])
def create():
    username = request.form['username']
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    u = user.User(
        name=username, fullname=fullname,email=email,password=hashed_password
    )

    if u.save():
        flash('Successfully created')
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', username = request.form['username'], fullname = request.form['fullname'], email = request.form['email'], password = request.form['password'], errors=u.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"
    

@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

