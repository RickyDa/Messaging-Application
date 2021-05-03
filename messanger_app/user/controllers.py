from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user
from .logic import *

auth = Blueprint('auth', __name__)


@auth.route('/user/signup', methods=['POST'])
def signup_user():
    user_form = request.form
    rv, res = create_new_user(user_form)
    return jsonify({"result": rv}), res


@auth.route('/user/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'error': 'already logged in'}), 400

    login_form = request.form
    authed_user = validate_login_info(username=login_form['username'], password=login_form['password'])
    if authed_user:
        login_user(authed_user)
        return jsonify({'result': 'logged in successfully'}), 200
    else:
        return jsonify({'error': 'incorrect password or email'}), 400


@auth.route("/user/logout", methods=['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        return jsonify({'error': 'not logged in yet'}), 400
    logout_user()
    return jsonify({'Success': 'logged out'}), 200


@auth.route('/')
def hello():
    if current_user.is_authenticated:
        return jsonify({'msg': f'Hello {current_user.username}!'}), 200
    return jsonify({'msg': f'Hello!'}), 200
