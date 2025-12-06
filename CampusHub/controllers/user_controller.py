from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from CampusHub.models.event_model import Event
from CampusHub.models.notification_model import Notification

user_bp = Blueprint('user', __name__)

@user_bp.app_context_processor
def inject_notifications():
    """Inject unread notifications count into all templates"""
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        recent_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date_created.desc()).limit(5).all()
        return dict(unread_notifications_count=unread_count, recent_notifications=recent_notifications)
    return dict(unread_notifications_count=0, recent_notifications=[])

@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        # Calculate statistics for admin dashboard
        total_users = User.query.count()
        total_events = Event.query.count()
        pending_events = Event.query.filter_by(is_approved=False).count()
        return render_template('admin/dashboard.html', 
                             user=current_user,
                             total_users=total_users,
                             total_events=total_events,
                             pending_events=pending_events)
    return render_template('user/dashboard.html', user=current_user)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        
        if not email:
            flash('Email is required.', 'error')
            return redirect(url_for('user.profile'))
            
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Email already registered.', 'error')
            return redirect(url_for('user.profile'))
            
        current_user.email = email
        if username:
            current_user.username = username
            
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating profile.', 'error')
            
        return redirect(url_for('user.profile'))
        
    return render_template('user/profile.html', user=current_user)

@user_bp.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html', user=current_user)

@user_bp.route('/notifications/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    return redirect(request.referrer or url_for('user.dashboard'))
