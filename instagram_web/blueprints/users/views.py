from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash
from models.user import User
from flask_login import current_user

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
        return redirect(url_for('users.new', id=u.id))
    else:
        return render_template('users/new.html', name=request.form['name'], errors=u.errors)


@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    return redirect(url_for('users.new'))


# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"


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
    password_edit = request.form.get('password_edit')
    email_edit = request.form.get('email_edit')

    user = User.get_by_id(id)
    user.name = name_edit
    user.password = password_edit
    user.email = email_edit

    if user.save():
        flash('Update Successful')
        return redirect(url_for('users.edit', id=user.id))
    else:
        flash('Update Fail')
        return render_template('home.html')


# @users_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass


# @users_blueprint.route('/<id>', methods=['POST'])
# def update(id):
#     pass
