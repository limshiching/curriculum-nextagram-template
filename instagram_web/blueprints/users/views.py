from flask_wtf.csrf import CSRFProtect
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape
from models.user import User
from models.image import Image
from models import *
from flask_login import current_user
from instagram_web.util.helpers import upload_file_to_s3
import os


app = Flask(__name__)


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

    u = user.User(
        name=username, fullname=fullname,email=email,password=password
    )

    if u.save():
        flash('Successfully created')
        return redirect(url_for('users.new'))
    else:
        return render_template('new.html', username = request.form['username'], fullname = request.form['fullname'], email = request.form['email'], password = request.form['password'], errors=u.errors)


@users_blueprint.route('/', methods=["GET"])
def index():
    user = User.select()

    return render_template('home.html', user=user)


@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    user = User.get_or_none(User.id == id)

    if not user:
        return redirect(url_for('home'))

    return render_template('users/show.html', user=user)


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action
    if current_user ==  user: 
        return render_template('users/edit.html', id=user.id, user=user)
    
    return redirect(url_for('home'))


@users_blueprint.route('/users/<id>', methods=['POST'])
def update(id):
    name_edit = request.form.get('name')
    email_edit = request.form.get('email')
    
    user = User.get_by_id(id)
    
    user.name = name_edit
    user.email = email_edit

    if user.save():
        flash('Successfully updated')
        return redirect(url_for('users.edit', id=user.id))

    else:
        return render_template('users/edit.html')

    if not user:
        return redirect(url_for('home'))


@users_blueprint.route('/user/upload', methods=['POST'])
def upload():

    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]

    user = User.get_or_none(User.id == current_user.id)

    if file.filename == "":
        return "Please select a file"

    if user:
        output = upload_file_to_s3(file, os.environ.get("S3_BUCKET"))
        user.profile_image = file.filename

    if user.save():
        flash('Successfully uploaded profile picture!')
        return redirect(url_for('images.new'))
        
    else:
        return render_template('images/new.html')





