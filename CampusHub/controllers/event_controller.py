from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from CampusHub.models.event_model import Event
from CampusHub.models.notification_model import Notification
from CampusHub.extensions import db
from CampusHub.helpers import log_activity
from datetime import datetime

event_bp = Blueprint('event', __name__)

@event_bp.route('/')
@event_bp.route('/')
def list_events():
    # Admins see all events, others see only approved events
    if current_user.is_authenticated and current_user.role == 'admin':
        events = Event.query.order_by(Event.date.asc()).all()
    else:
        events = Event.query.filter_by(is_approved=True).order_by(Event.date.asc()).all()
    return render_template('event/list.html', events=events)

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.role not in ['admin', 'teacher', 'instructor']:
        flash('You do not have permission to create events.', 'error')
        return redirect(url_for('event.list_events'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        location = request.form.get('location')
        capacity = request.form.get('capacity', type=int)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('event/create.html')

        event = Event(
            title=title,
            description=description,
            date=date,
            location=location,
            capacity=capacity if capacity else 3,
            creator=current_user,
            is_approved=False  # Changed to require admin approval
        )
        db.session.add(event)
        db.session.commit()
        log_activity(current_user.id, 'EVENT_CREATED', f'Event "{title}" created')
        flash('Event created successfully! Waiting for admin approval.')
        return redirect(url_for('event.list_events'))

    return render_template('event/create.html')

@event_bp.route('/<int:event_id>/register', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if current_user in event.attendees:
        flash('You are already registered for this event.')
    else:
        # Check capacity
        if event.is_full:
            flash('Sorry, this event has reached its maximum capacity.', 'error')
        else:
            event.attendees.append(current_user)
            db.session.commit()
            flash('Successfully registered for event!')
        
    return redirect(url_for('event.list_events'))

@event_bp.route('/<int:event_id>/unregister', methods=['POST'])
@login_required
def unregister_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if current_user in event.attendees:
        event.attendees.remove(current_user)
        db.session.commit()
        flash('Successfully unregistered from the event.')
    else:
        flash('You are not registered for this event.', 'error')
        
    return redirect(url_for('event.list_events'))

@event_bp.route('/<int:event_id>')
@login_required
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event/details.html', event=event)

@event_bp.route('/<int:event_id>/approve', methods=['POST'])
@login_required
def approve_event(event_id):
    if current_user.role != 'admin':
        flash('You do not have permission to approve events.', 'error')
        return redirect(url_for('event.list_events'))
    
    event = Event.query.get_or_404(event_id)
    event.is_approved = True
    db.session.commit()
    
    # Create notification for event creator
    notification = Notification(
        user_id=event.creator_id,
        message=f'Your event "{event.title}" has been approved by an admin!'
    )
    db.session.add(notification)
    db.session.commit()
    
    log_activity(current_user.id, 'EVENT_APPROVED', f'Event "{event.title}" approved')
    flash(f'Event "{event.title}" has been approved!')
    
    return redirect(url_for('event.list_events'))

@event_bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    if current_user.role != 'admin':
        flash('You do not have permission to delete events.', 'error')
        return redirect(url_for('event.list_events'))
    
    event = Event.query.get_or_404(event_id)
    event_title = event.title
    db.session.delete(event)
    db.session.commit()
    log_activity(current_user.id, 'EVENT_DELETED', f'Event "{event_title}" deleted')
    flash(f'Event "{event_title}" has been deleted.')
    
    return redirect(url_for('event.list_events'))
