from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '779f42b478a05a759a4028553a2fdae3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ricky@localhost:5432/MessagingApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# from message_delete import routes as message_routes
# from user_delete import routes as user_routes
from .user import controllers as usr_control
from .message import controllers as usr_control

db.create_all()
