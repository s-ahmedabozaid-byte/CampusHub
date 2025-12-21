from CampusHub.extensions import db
from CampusHub.models.log_model import Log

def log_activity(user_id, action, details=None):
    """
    Helper function to log user activities
    
    Args:
        user_id: ID of the user performing the action (can be None for system actions)
        action: Type of action (e.g., 'LOGIN', 'EVENT_CREATED', 'USER_DELETED')
        details: Additional details about the action
    """
    try:
        log = Log(user_id=user_id, action=action, details=details)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error logging activity: {e}")
