from messanger_app import db, login_manager
from flask_login import UserMixin

subscribers = db.Table('subscribers',
                       db.Column('users_id', db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
                       db.Column('message_id', db.Integer, db.ForeignKey("messages.id", ondelete="CASCADE"))
                       , schema='public')


@login_manager.user_loader
def load_user(_id):
    return User.query.get(_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, default=db.func.now())
    messages = db.relationship(
        "Message",
        secondary=subscribers,
        back_populates="subscribers",
        cascade="all, delete",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<User {self.id}: ('{self.username}','{self.email}'')>"

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(40), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=db.func.now())
    subscribers = db.relationship(
        "User",
        secondary=subscribers,
        back_populates="messages",
        passive_deletes=True, lazy="dynamic"
    )

    def __repr__(self):
        return f"<Message {self.id}: (To: {self.receiver_id}, From: {self.sender} Subject: {self.subject})>"

    def serialize(self):
        return {
            'message_id': self.id,
            'sender': self.sender,
            'subject': self.subject,
            'body': self.body,
            'read': self.read,
            'created': self.created}

    @classmethod
    def from_json(cls, data):
        return cls(**data)
