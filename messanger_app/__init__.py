from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# define flaks extensions
bcrypt = Bcrypt()  # for encryption/ decryption
db = SQLAlchemy()  # for handling database
login_manager = LoginManager()  # for handling user sessions

from .user.controllers import auth
from .message.controllers import main


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '779f42b478a05a759a4028553a2fdae3'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ricky@localhost:5432/MessagingApp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app



