from flask import jsonify, request, Blueprint, make_response
from flask_jwt_extended import create_access_token
from models.user import User
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint(
    'sessions_api', 
    __name__, 
    template_folder='templates'
)

@sessions_api_blueprint.route('/', methods=['POST'])
def create():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_or_none(User.username == username)

    if not user:
        response = {
            'message': 'No user exists'
        }

        return make_response(jsonify(response), 401)

    if not check_password_hash:
        response = {
            'message': 'Password invalid'
        }

        return make_response(jsonify(response), 401)

    access_token = create_access_token(identity=user.id)

    response = {
        'message': 'login successfully',
        'auth_token': access_token
    }

    return make_response(jsonify(response), 200)
