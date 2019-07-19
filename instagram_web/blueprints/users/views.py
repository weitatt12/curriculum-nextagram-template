from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash
from models.user import User

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


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return redirect(url_for('users.new'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
