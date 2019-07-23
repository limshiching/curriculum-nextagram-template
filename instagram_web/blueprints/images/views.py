import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, escape
from models.user import User
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates/')
                            
@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')

@images_blueprint.route('/create', methods=['POST'])
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
        return str(output)

        
    else:
        return redirect("/")