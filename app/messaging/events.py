from flask import session, request
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
from .models import Message, Chat
from app.extensions import db
from app.models import User
from .utils import get_room_code

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print(f"Client connected: {request.sid}")

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Client disconnected: {request.sid}")
        
    @socketio.on('join')
    def handle_join(data):
        room = data.get('room')
        name = data.get('name', 'Unknown User')
        user_type = data.get('userType')
        
        # Join the room
        join_room(room)
        
        # If a patient is initiating a chat with a doctor
        if user_type == 'patient' and 'doctorId' in data:
            doctor_id = data.get('doctorId')
            patient_id = session.get('user_id')
            
            # Check if chat already exists
            chat = Chat.query.filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
            if not chat:
                # Create a new chat
                chat = Chat(doctor_id=doctor_id, patient_id=patient_id)
                db.session.add(chat)
                db.session.commit()
            
            # Generate room code for consistency
            room_code = get_room_code(doctor_id, patient_id)
            
            # Notify doctor that a patient wants to chat (special event)
            emit('patient_connected', {
                'room': room_code,
                'name': name,
                'patientId': patient_id,
                'message': f"Patient {name} wants to chat"
            }, room=f"doctor_{doctor_id}")
        
        # Send system message to room that user has joined
        emit('system', {
            'message': f"{name} has entered the chat",
            'userType': user_type,
            'name': name,
            'room': room
        }, room=room)
        
        print(f"User {name} ({user_type}) joined room: {room}")

    @socketio.on('leave')
    def handle_leave(data):
        room = data.get('room')
        if room:
            leave_room(room)
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            name = user.name if user else f"User-{user_id}"
            user_type = user.role if user else 'unknown'
            
            emit('system', {
                'message': f"{name} has left the chat",
                'userType': user_type,
                'name': name,
                'room': room
            }, room=room)
            
            print(f"User {name} ({user_type}) left room: {room}")

    @socketio.on('message')
    def handle_message(data):
        room = data.get('room')
        message_text = data.get('data')
        user_type = data.get('userType')
        name = data.get('name', 'Unknown User')
        user_id = session.get('user_id')
        
        if not room:
            print("Error: No room specified in message data")
            return
        
        # Parse room code to get doctor and patient IDs
        parts = room.split('_')
        if len(parts) == 3 and parts[0] == 'chat':
            doctor_id = int(parts[1])
            patient_id = int(parts[2])
            
            # Get the chat ID
            chat = Chat.query.filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
            
            if not chat:
                # Create a new chat if it doesn't exist
                chat = Chat(doctor_id=doctor_id, patient_id=patient_id)
                db.session.add(chat)
                db.session.commit()
            
            # Save message to database
            new_message = Message(
                chat_id=chat.id,
                user_id=user_id,
                content=message_text,
                timestamp=datetime.utcnow()
            )
            db.session.add(new_message)
            db.session.commit()
        
        # Get user details for message attribution
        user = User.query.get(user_id)
        if user:
            name = user.name or name
        
        # Broadcast the message to everyone in the room
        emit('message', {
            'message': message_text,
            'userType': user_type,
            'name': name,
            'userId': user_id,
            'room': room,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }, room=room)

    @socketio.on('end_session')
    def handle_end_session(data):
        room = data.get('room')
        if room:
            # Send system message that the session has ended
            emit('system', {
                'message': 'This chat session has ended',
                'room': room
            }, room=room)
            
            print(f"Chat session ended in room: {room}")