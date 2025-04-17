from app.extensions import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chats'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, archived, ended
    
    # Define relationships
    messages = db.relationship('Message', backref='chat', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Chat {self.id}: Doctor {self.doctor_id} - Patient {self.patient_id}>"

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Message {self.id}: Chat {self.chat_id}>"

# This model could be used to track who's read which messages in a chat
class MessageStatus(db.Model):
    __tablename__ = 'message_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"<MessageStatus: Message {self.message_id} - User {self.user_id}>"