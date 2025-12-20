from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from CampusHub.models.announcement_model import Announcement
from CampusHub.extensions import db
from CampusHub.helpers import log_activity

announcement_bp = Blueprint('announcement', __name__)

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

# Admin Routes
@announcement_bp.route('/admin/announcements')
@login_required
@admin_required
def admin_list():
    """List all announcements for admin"""
    announcements = Announcement.query.order_by(Announcement.date_created.desc()).all()
    return render_template('admin/announcement/list.html', announcements=announcements)

@announcement_bp.route('/admin/announcements/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create new announcement"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_published = request.form.get('is_published') == 'on'
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('announcement.create'))
        
        announcement = Announcement(
            title=title,
            content=content,
            is_published=is_published,
            creator=current_user
        )
        db.session.add(announcement)
        db.session.commit()
        
        log_activity(current_user.id, 'ANNOUNCEMENT_CREATED', f'Announcement "{title}" created')
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('announcement.admin_list'))
    
    return render_template('admin/announcement/create.html')

@announcement_bp.route('/admin/announcements/<int:announcement_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_published(announcement_id):
    """Toggle announcement published status"""
    announcement = Announcement.query.get_or_404(announcement_id)
    announcement.is_published = not announcement.is_published
    db.session.commit()
    
    status = 'published' if announcement.is_published else 'unpublished'
    log_activity(current_user.id, 'ANNOUNCEMENT_TOGGLED', f'Announcement "{announcement.title}" {status}')
    flash(f'Announcement has been {status}.', 'success')
    
    return redirect(url_for('announcement.admin_list'))

@announcement_bp.route('/admin/announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(announcement_id):
    """Delete announcement"""
    announcement = Announcement.query.get_or_404(announcement_id)
    title = announcement.title
    db.session.delete(announcement)
    db.session.commit()
    
    log_activity(current_user.id, 'ANNOUNCEMENT_DELETED', f'Announcement "{title}" deleted')
    flash(f'Announcement "{title}" has been deleted.', 'success')
    
    return redirect(url_for('announcement.admin_list'))

# User Routes
@announcement_bp.route('/announcements')
@login_required
def list_announcements():
    """View published announcements"""
    announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.date_created.desc()).all()
    return render_template('announcement/list.html', announcements=announcements)
