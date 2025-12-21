from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from CampusHub.extensions import db
from CampusHub.models.feedback_model import Feedback
from CampusHub.helpers import log_activity

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/send', methods=['POST'])
@login_required
def send_feedback():
    message = request.form.get('message')
    category = request.form.get('category')
    
    if not message or not category:
        flash('Please provide both category and message.', 'error')
        # Redirect back to where they came from or dashboard
        return redirect(request.referrer or url_for('user.dashboard'))
        
    feedback = Feedback(
        user_id=current_user.id,
        message=message,
        category=category
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    # Log activity
    log_activity(current_user.id, 'FEEDBACK_SENT', f'User sent {category} feedback')
    
    flash('Thank you for your feedback!', 'success')
    return redirect(request.referrer or url_for('user.dashboard'))
