from messanger_app.database.models import User, Message
from messanger_app.database.db_ops import create, update, delete
from flask_login import current_user
from sqlalchemy import not_, and_


def create_new_message(msg):
    receiver = User.query.filter_by(username=msg['receiver']).first()
    del msg['receiver']

    msg['receiver_id'] = receiver.id
    msg['sender'] = current_user.username
    msg = Message.from_json(msg)

    msg.subscribers.append(current_user)
    msg.subscribers.append(receiver)
    msg = create(msg)
    return msg


def get_all_messages():
    return [msg.serialize() for msg in current_user.messages.all()]


def get_all_unread_messages():
    return [msg.serialize() for msg in
            current_user.messages.filter(and_(Message.receiver_id == current_user.id, not_(Message.read))).all()]


def mark_as_read(msg):
    msg.read = True
    update()
    return msg


def read_message(_id):
    msg = current_user.messages.filter_by(id=_id).first()
    if msg.read:
        return msg.serialize()
    else:
        return mark_as_read(msg).serialize()


def delete_message_by_id(_id):
    msg = current_user.messages.filter_by(id=_id).first()
    msg.subscribers.remove(current_user)
    update()
    if msg.subscribers.count() == 0:
        delete(msg)
