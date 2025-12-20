from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from CampusHub.extensions import db
from CampusHub.models.task_model import Task
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route('/', methods=['GET'])
@login_required
def list_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks, now=datetime.utcnow())

@task_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    deadline_str = request.form.get('deadline')
    
    if not title:
        flash('Title is required.', 'error')
        return redirect(url_for('task.list_tasks'))
        
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('task.list_tasks'))
            
    task = Task(
        title=title,
        description=description,
        deadline=deadline,
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    flash('Task created successfully!', 'success')
    
    return redirect(url_for('task.list_tasks'))

@task_bp.route('/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('Permission denied.', 'error')
        return redirect(url_for('task.list_tasks'))
        
    if task.status == 'Pending':
        task.status = 'Completed'
    else:
        task.status = 'Pending'
        
    db.session.commit()
    return redirect(url_for('task.list_tasks'))
