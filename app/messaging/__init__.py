from flask import Blueprint, render_template, session, request, jsonify
from .events import register_socket_events
from .models import Message, Chat
from app.extensions import db, socketio
from app.models import User
from .utils import get_room_code
from .decorators import login_required

messaging_bp = Blueprint('messaging', __name__, url_prefix='/messaging')

@messaging_bp.route('/patient')
@login_required
def patient_messaging():
    # Get available doctors
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('patient_messaging.html', 
                          doctors=doctors,
                          user_id=session.get('user_id'),
                          name=session.get('name', 'Patient'))

@messaging_bp.route('/doctor')
@login_required
def doctor_messaging():
    # Get list of patients who have messaged this doctor
    doctor_id = session.get('user_id')
    
    # Get chats where this doctor is a participant
    chats = Chat.query.filter_by(doctor_id=doctor_id).all()
    
    # Get the patients involved in these chats
    patients = []
    for chat in chats:
        patient = User.query.filter_by(id=chat.patient_id).first()
        if patient:
            # Get the last message in this chat
            last_message = Message.query.filter_by(chat_id=chat.id).order_by(Message.timestamp.desc()).first()
            
            patients.append({
                'id': patient.id,
                'name': patient.name or f"Patient-{patient.id}",
                'chat_id': chat.id,
                'room_code': get_room_code(doctor_id, patient.id),
                'last_message': last_message.content if last_message else None,
                'last_timestamp': last_message.timestamp if last_message else None
            })
    
    # Sort by latest message
    patients = sorted(patients, key=lambda x: x['last_timestamp'] if x['last_timestamp'] else 0, reverse=True)
    
    return render_template('doctor_messaging.html', 
                          patients=patients,
                          user_id=session.get('user_id'),
                          name=session.get('name', 'Doctor'))

@messaging_bp.route('/chat/<doctor_id>')
@login_required
def get_chat(doctor_id):
    patient_id = session.get('user_id')
    
    # Get or create chat
    chat = Chat.query.filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
    if not chat:
        chat = Chat(doctor_id=doctor_id, patient_id=patient_id)
        db.session.add(chat)
        db.session.commit()
    
    # Get previous messages
    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.timestamp).all()
    
    # Format messages for frontend
    formatted_messages = []
    for msg in messages:
        user = User.query.get(msg.user_id)
        user_type = 'doctor' if user.role == 'doctor' else 'patient'
        formatted_messages.append({
            'id': msg.id,
            'message': msg.content,
            'userType': user_type,
            'name': user.name or (f"Dr. {user.id}" if user_type == 'doctor' else f"Patient-{user.id}"),
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Generate room code
    room_code = get_room_code(doctor_id, patient_id)
    
    # Get doctor info
    doctor = User.query.get(doctor_id)
    doctor_name = doctor.name if doctor else f"Dr. {doctor_id}"
    
    return jsonify({
        'messages': formatted_messages,
        'room_code': room_code,
        'chat_id': chat.id,
        'doctor_name': doctor_name
    })

@messaging_bp.route('/messages/<chat_id>', methods=['GET'])
@login_required
def get_messages(chat_id):
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    
    formatted_messages = []
    for msg in messages:
        user = User.query.get(msg.user_id)
        user_type = 'doctor' if user.role == 'doctor' else 'patient'
        formatted_messages.append({
            'id': msg.id,
            'message': msg.content,
            'userType': user_type,
            'name': user.name or (f"Dr. {user.id}" if user_type == 'doctor' else f"Patient-{user.id}"),
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(formatted_messages)

def init_app(app):
    app.register_blueprint(messaging_bp)
    register_socket_events(socketio)