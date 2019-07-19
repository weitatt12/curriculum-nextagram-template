from flask import Blueprint, render_template, url_for, redirect, request, flash, Flask, session
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from models.user import User

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates/sessions'
)


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('/new.html')


@sessions_blueprint.route('/create', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_or_none(User.username == username)
    if not user:
        flash('username invalid')
        return redirect(url_for('sessions.new'))

    if not check_password_hash(user.password, password):
        flash('password invalid')
        return redirect(url_for('sessions.new'))

    # Log in the user
    login_user(user)
    # flash a welcome message
    flash('Login successfuly')
    # redirect them to a page
    return redirect(url_for('home'))


@sessions_blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logout Successful')
    return redirect(url_for('home'))
