from app import app, csrf
from flask_cors import CORS
from flask_jwt_extended import JWTManager

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config[''] = 'secret-key'
jwt = JWTManager(app)


## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
from instagram_api.blueprints.sessions.view import sessions_api_blueprint

app.register_blueprint(csrf.exempt(users_api_blueprint), url_prefix='/api/v1/users')
app.register_blueprint(csrf.exempt(sessions_api_blueprint), url_prefix='/api/v1/sessions')

# csrf.exempt(users_api_blueprint)
# csrf.exempt(sessions_api_blueprint)