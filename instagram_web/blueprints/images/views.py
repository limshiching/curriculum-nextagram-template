import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape
from models.user import User
from models.image import Image
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from flask_login import current_user

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates/')
                            
@images_blueprint.route('/new', methods=['GET'])
def new():
    users = User.select()
    return render_template('images/new.html', users=users)

@images_blueprint.route('/images/create', methods=['POST'])
def create():

    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file    = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, os.environ.get("S3_BUCKET"))
        flash('Successfully uploaded image!')

        image = Image(user = current_user.id,image_path=str(output))

    if image.save():
        return redirect(url_for('images.new'))
        
    else:
        return render_template('images/new.html')


@images_blueprint.route('/<name>', methods=["GET"])
def show(name):
    user = User.get(User.name == name)
    images = Image.select().where(Image.user==user)

    return render_template('images/show.html', user=user, images=images)

        
  


