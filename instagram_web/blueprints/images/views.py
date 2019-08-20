import os
from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3
from models.user import User
from models.image import Image
from flask_login import current_user

images_blueprint = Blueprint(
    'images', __name__, template_folder='templates/'
)


@images_blueprint.route('/new', methods=["GET"])
def new():
    return render_template("images/new.html")


@images_blueprint.route("/images/create", methods=["POST"])
def create():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files.get("user_file")

    if file.filename == "":
        return "Please select a file"

    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, os.environ.get("S3_BUCKET"))

        image = Image(user=current_user.id, image_path=file.filename)

        if image.save():
            flash('Upload Successful')
            return redirect(url_for('images.new'))

    else:
        return redirect("/")
