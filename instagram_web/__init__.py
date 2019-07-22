from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error_code=500, message="Internal Server Error")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_code=404, message="Page Not Found")


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', error_code=403, message="Forbidden")


@app.errorhandler(410)
def gone(e):
    return render_template('410.html', error_code=410, message="Gone")

@app.route("/")
def home():
    return render_template('home.html')
