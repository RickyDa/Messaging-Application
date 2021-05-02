import re
from messanger_app import bcrypt
from messanger_app.database.models import User
from messanger_app.database.db_ops import create


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email_as_str = str(email)
    if re.match(regex, email_as_str) is not None:
        match_user = User.query.filter_by(email=email).first()
        if match_user is not None:
            raise Exception('Email Already Exists!')
    else:
        raise Exception('Not a Valid Email!')


def validate_login_info(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    else:
        return


def validate_username(username):
    username = str(username)
    match_user = User.query.filter_by(username=username).first()
    if match_user is not None:
        raise Exception('User Name Already Exists!')


def encrypt(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def create_new_user(user):
    user = User.from_json(user)
    try:
        validate_username(user.username)
        validate_email(user.email)
        user.password = encrypt(user.password)
        user = create(user)
        if not user:
            return 'Something went wrong please try again', 400
        return user.id, 200
    except Exception as e:
        return str(e), 400
