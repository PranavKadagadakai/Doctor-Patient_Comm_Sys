from flask_socketio import emit, join_room
from flask_jwt_extended import decode_token
from ..extensions import socketio, db
from .models import Message
from flask import request
import os
import uuid

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    try:
        user = decode_token(token)['sub']
        join_room(user['id'])
        emit('connected', {'msg': 'Socket connection established'})
    except Exception as e:
        return False  # reject connection

@socketio.on('send_message')
def handle_message(data):
    sender = decode_token(data['token'])['sub']
    recipient_id = data.get('recipient_id')
    message_text = data.get('message')
    file_data = data.get('file')  # Optional

    file_url = None
    if file_data:
        filename = f"{uuid.uuid4().hex}.txt"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(file_data)  # In real app, decode from base64 or accept file uploads
        file_url = f"/uploads/{filename}"

    message = Message(sender_id=sender['id'], recipient_id=recipient_id,
                      message=message_text, file_url=file_url)
    db.session.add(message)
    db.session.commit()

    emit('receive_message', {
        'sender_id': sender['id'],
        'message': message_text,
        'file_url': file_url,
        'timestamp': message.timestamp.isoformat()
    }, room=recipient_id)
