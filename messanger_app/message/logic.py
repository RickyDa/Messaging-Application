from messanger_app.database.models import User, Message
from messanger_app.database.db_ops import create, update, delete
from flask_login import current_user
from sqlalchemy import not_, and_


def create_new_message(msg):
    """
    Creating a new messages and assign the users to the subscribers relation table.
    :param msg: dict structure of the msg
    :return: Message object
    """
    receiver = User.query.filter_by(username=msg['receiver']).first()
    del msg['receiver']

    msg['receiver_id'] = receiver.id
    msg['sender'] = current_user.username
    msg = Message.from_json(msg)

    msg.subscribers.append(current_user)

    if current_user.id != receiver.id:
        msg.subscribers.append(receiver)

    msg = create(msg)
    return msg


def get_all_messages():
    """
    Get all messages that are sent by the user or got from other users
    :return: list of serialized Message objects
    """
    return [msg.serialize() for msg in current_user.messages.all()]


def get_all_unread_messages():
    """
    Get all unread messages[read == False] that the user received
    :return: list of serialized Message objects
    """
    return [msg.serialize() for msg in
            current_user.messages.filter(and_(Message.receiver_id == current_user.id, not_(Message.read))).all()]


def mark_as_read(msg):
    """
    Mark message object as read by updating their read status.
    :param msg: Message
    :return: Message
    """
    msg.read = True
    update()
    return msg


def read_message(_id):
    """
    Get specific message from db by its id and mark it as read.
    :param _id: Integer
    :return: serialized Message object
    """
    msg = current_user.messages.filter(Message.id == _id).first()
    if not msg:
        return None
    if msg.read or msg.sender == current_user.username:
        return msg.serialize()
    else:
        return mark_as_read(msg).serialize()


def delete_message_by_id(_id):
    """
    Delete specific message (by id) from the user's messages (relation table (subscribers)), if the message
    has no subscribers the Message will be deleted from the db.
    :param _id: Integer
    :return: Boolean
    """
    msg = current_user.messages.filter_by(id=_id).first()
    if not msg:
        return False
    msg.subscribers.remove(current_user)
    update()
    if msg.subscribers.count() == 0:
        delete(msg)
    return True
