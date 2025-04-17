def get_room_code(doctor_id, patient_id):
    """
    Generate a consistent room code for a chat between a doctor and patient.
    Format: chat_[doctor_id]_[patient_id]
    
    Args:
        doctor_id (int): The doctor's user ID
        patient_id (int): The patient's user ID
    
    Returns:
        str: A room code string
    """
    return f"chat_{doctor_id}_{patient_id}"

def is_user_doctor(user):
    """
    Check if a user is a doctor
    
    Args:
        user: The user object
    
    Returns:
        bool: True if user is a doctor, False otherwise
    """
    return user and user.role == 'doctor'

def is_user_patient(user):
    """
    Check if a user is a patient
    
    Args:
        user: The user object
    
    Returns:
        bool: True if user is a patient, False otherwise
    """
    return user and user.role == 'patient'

def format_timestamp(timestamp):
    """
    Format a timestamp for display
    
    Args:
        timestamp: A datetime object
    
    Returns:
        str: A formatted timestamp string
    """
    if not timestamp:
        return ""
    
    return timestamp.strftime("%H:%M %p, %b %d")

def get_unread_message_count(chat_id, user_id):
    """
    Get the number of unread messages in a chat for a specific user
    
    Args:
        chat_id (int): The chat ID
        user_id (int): The user ID
    
    Returns:
        int: The number of unread messages
    """
    from .models import Message
    from app.models import User
    
    user = User.query.get(user_id)
    if not user:
        return 0
    
    # If doctor, count patient messages that are unread
    # If patient, count doctor messages that are unread
    if user.role == 'doctor':
        # Get messages sent by patients that are unread
        from app.models import User
        from sqlalchemy import and_
        
        # Get the patient ID for this chat
        from .models import Chat
        chat = Chat.query.get(chat_id)
        if not chat:
            return 0
        
        # Count unread messages
        return Message.query.join(User).filter(
            and_(
                Message.chat_id == chat_id,
                User.id == Message.user_id,
                User.role == 'patient',
                Message.read == False
            )
        ).count()
    else:
        # Get messages sent by doctors that are unread
        from app.models import User
        from sqlalchemy import and_
        
        return Message.query.join(User).filter(
            and_(
                Message.chat_id == chat_id,
                User.id == Message.user_id,
                User.role == 'doctor',
                Message.read == False
            )
        ).count()