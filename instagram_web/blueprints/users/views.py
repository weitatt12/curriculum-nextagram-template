from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash
from models.user import User
from flask_login import current_user
from instagram_web.util.helpers import upload_file_to_s3
import os

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    u = User(name=name, email=email, username=username,
             password=password)
    if u.save():
        flash("Successfully Saved")
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if not user:
        render_template('home.html')
    else:

        return render_template('users/show.html', user=user)


@users_blueprint.route('/', methods=["GET"])
def index():
    user = User.select()
    return render_template("home.html")


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)

    if current_user == user:
        return render_template('users/edit.html', id=user.id, user=user)

    if current_user != user:
        flash('Unauthorized to perform this action')
        return render_template('users/new.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    name_edit = request.form.get('name_edit')
    email_edit = request.form.get('email_edit')
    private_edit = request.form.get('private_edit')
    # password_edit = request.form.get('password_edit')

    user = User.get_by_id(id)
    user.name = name_edit
    user.email = email_edit
    # user.password = password_edit

    if request.form.get('private'):
        user.private = True
        if user.save():
            flash('Update Successful')
            return redirect(url_for('users.edit', id=user.id))
        else:
            return redirect(url_for('users.edit', id=user.id))
    else:
        user.private = False
        if user.save():
            flash('Successfully update')
            return redirect(url_for('users.edit', id=user.id))
        else:
            return render_template('home.html')


@users_blueprint.route('/upload', methods=['GET'])
def pic():
    return render_template('users/new.html')


@users_blueprint.route('/upload_pp', methods=['POST'])
def pro_picture():
    file = request.files.get("profile_image")

    user = User.get_or_none(User.id == current_user.id)

    if file.filename == "":
        return "Please select a file"

    if user:
        output = upload_file_to_s3(file, os.environ.get("S3_BUCKET"))
        # user.profile_image = file.filename
        User.update(profile_image=output).where(
            User.id == current_user.id).execute()
        flash('Upload Successful')
        return redirect(url_for('users.show', username=user.username))
    return redirect(url_for('user.new'))
