from messanger_app import app
from flask import request, jsonify
from flask_login import login_required
from .logic import *


@app.route('/message/send', methods=['POST'])
@login_required
def send():
    message_form = request.form.to_dict()
    dest = message_form['receiver']
    msg = create_new_message(message_form)
    if msg is None:
        return jsonify({'result': 'Error occurred while sending this message try again'}), 500
    return jsonify({'result': f"message sent to {dest}"}), 200


@app.route('/message/all', methods=['GET'])
@login_required
def get_all():
    return jsonify(get_all_messages()), 200


@app.route('/message/unread', methods=['GET'])
@login_required
def get_unread():
    return jsonify(get_all_unread_messages()), 200


@app.route('/message/<_id>', methods=['GET'])
@login_required
def get_message(_id):
    return jsonify(read_message(_id)), 200


@app.route('/message/delete/<_id>', methods=['DELETE'])
@login_required
def delete_message(_id):
    delete_message_by_id(_id)
    return jsonify({'result': f"unsubscribed from message"}), 200
