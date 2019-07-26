from flask import Blueprint, render_template, url_for, redirect, request, flash, Flask, session
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from models.user import User
from instagram_web.util.google_helper import oauth

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
    flash(f'Hi {current_user.name},Login successfuly')
    # redirect them to a page
    return redirect(url_for('home'))


@sessions_blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logout Successful')
    return redirect(url_for('home'))


@sessions_blueprint.route('/login_google', methods=["GET"])
def login_google():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google', methods=["GET"])
def authorize():
    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

        user = User.get_or_none(User.email == email)  # check database for user

        if not user:
            flash('Log in fail.')
            return redirect(url_for('sessions.new'))

    login_user(user)
    flash("login successful")
    return redirect(url_for("users.show", username=user.username))
