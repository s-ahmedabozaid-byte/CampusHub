from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from CampusHub.models.user_model import User
from CampusHub.models.event_model import Event
from CampusHub.models.event_model import Event
from CampusHub.models.log_model import Log
from CampusHub.models.feedback_model import Feedback
from CampusHub.models.task_model import Task
from CampusHub.extensions import db
from CampusHub.helpers import log_activity

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to ensure only admins can access routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    total_users = User.query.count()
    total_events = Event.query.count()
    pending_events = Event.query.filter_by(is_approved=False).count()
    total_feedbacks = Feedback.query.count()
    all_feedbacks = Feedback.query.all()
    
    print(f"ADMIN DEBUG: Found {len(all_feedbacks)} feedbacks")
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_events=total_events,
                         pending_events=pending_events,
                         total_feedbacks=total_feedbacks,
                         feedbacks=all_feedbacks)

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    """Admin reports and analytics"""
    total_users = User.query.count()
    total_feedbacks = Feedback.query.count()
    
    # Task Efficiency
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='Completed').count()
    task_completion_rate = 0
    if total_tasks > 0:
        task_completion_rate = round((completed_tasks / total_tasks) * 100, 1)
        
    # Top Event (by attendee count)
    # Since we can't easily sort by property in SQL without hybrid_property expression, 
    # and attendee_count is a property, we might need to fetch all and sort python side if dataset small, 
    # OR if we trust the loop logic. 
    # Wait, attendee_count is a property: return len(self.registrations).
    # Registrations are in EventRegistration model? 
    # Let's check Event model. Yes.
    # We can do a join count query for efficiency, or just fetch all for now (MVP).
    # events = Event.query.all()
    # top_event = max(events, key=lambda e: e.attendee_count) if events else None
    
    # Better approach: Join with registration count 
    # But for MVP let's use Python sort (dataset likely small)
    events = Event.query.all()
    top_event = None
    if events:
         top_event = max(events, key=lambda e: e.attendee_count)

    return render_template('admin/reports.html',
                         total_users=total_users,
                         total_feedbacks=total_feedbacks,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         task_completion_rate=task_completion_rate,
                         top_event=top_event)


@admin_bp.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/logs')
@login_required
@admin_required
def logs():
    """Display activity logs"""
    logs = Log.query.order_by(Log.timestamp.desc()).limit(100).all()
    return render_template('admin/logs.html', logs=logs)

@admin_bp.route('/users')
@login_required
@admin_required
def users_list():
    """Display list of all users"""
    # Exclude the currently logged-in admin user
    users = User.query.filter(User.id != current_user.id).order_by(User.email).all()
    return render_template('admin/users_list.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle_active', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(url_for('admin.users_list'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.email} has been {status}.')
    
    return redirect(url_for('admin.users_list'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users_list'))
    
    user_email = user.email
    db.session.delete(user)
    db.session.commit()
    log_activity(current_user.id, 'USER_DELETED', f'User {user_email} deleted')
    
    flash(f'User {user_email} has been deleted.')
    
    return redirect(url_for('admin.users_list'))
