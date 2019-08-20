from flask import Blueprint, jsonify, make_response
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

users_api_blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)    

@users_api_blueprint.route('/', methods=['GET'])
def new():
    users = User.select()

    user_list = []
    
    for user in users:
        user_list.append({
            'id' : user.id
            'full_name' : user.full_name
            'username' : user.username
            'profile_pic' : user.profile_url
        })

    response = {'data' : user_list}

    return make_response(jsonify(response), 200)

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def show():
    current_user = get_jwt_identity()

    user = User.get_or_none(User.id == current_user)

    user_data = {
        'id' : user.id,
        'username' : user.username
    }

    response = {
        'data' : user_data
    }

    return make_response(jsonify(response), 200)
