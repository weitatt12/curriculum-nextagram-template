from app import app
from flask import render_template
from instagram_web.util.google_helper import oauth
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)

from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.fans_idols.views import fans_idols_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(fans_idols_blueprint, url_prefix="/fans_idols")


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
