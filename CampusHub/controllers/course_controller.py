from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from CampusHub.extensions import db
from CampusHub.models.course_model import Course, enrollments
from CampusHub.models.user_model import User

course_bp = Blueprint('course', __name__)

@course_bp.route('/')
@login_required
def index():
    query = request.args.get('q')
    if query:
        courses = Course.query.filter(Course.title.ilike(f'%{query}%')).all()
    else:
        courses = Course.query.all()
    return render_template('courses/index.html', courses=courses, query=query)

@course_bp.route('/create', methods=['POST'])
@login_required
def create():
    if current_user.role != 'instructor' and current_user.role != 'admin':
        flash('Only instructors can create courses.', 'error')
        return redirect(url_for('course.index'))
        
    title = request.form.get('title')
    description = request.form.get('description')
    code = request.form.get('code')
    
    if not title or not code:
        flash('Title and Course Code are required.', 'error')
        return redirect(url_for('course.index'))
        
    # Check if code unique
    if Course.query.filter_by(code=code).first():
        flash('Course code already exists.', 'error')
        return redirect(url_for('course.index'))
        
    course = Course(title=title, description=description, code=code, instructor_id=current_user.id)
    db.session.add(course)
    db.session.commit()
    
    flash('Course created successfully!', 'success')
    return redirect(url_for('course.index'))

@course_bp.route('/<int:course_id>')
@login_required
def details(course_id):
    course = Course.query.get_or_404(course_id)
    is_enrolled = False
    if current_user.is_authenticated:
        # Check enrollment in association table
        # We can check using the relationship
        if course in current_user.enrolled_courses:
            is_enrolled = True
            
    return render_template('courses/details.html', course=course, is_enrolled=is_enrolled)

@course_bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    
    if course in current_user.enrolled_courses:
        flash('You are already enrolled.', 'info')
    else:
        current_user.enrolled_courses.append(course)
        db.session.commit()
        flash(f'Enrolled in {course.title} successfully!', 'success')
        
    return redirect(url_for('course.details', course_id=course_id))

@course_bp.route('/<int:course_id>/delete', methods=['POST'])
@login_required
def delete(course_id):
    course = Course.query.get_or_404(course_id)
    
    if current_user.id != course.instructor_id and current_user.role != 'admin':
        flash('Unauthorized', 'error')
        return redirect(url_for('course.index'))
        
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted.', 'success')
    return redirect(url_for('course.index'))

@course_bp.route('/<int:course_id>/assignments/create', methods=['POST'])
@login_required
def create_assignment(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.instructor_id:
        flash('Unauthorized', 'error')
        return redirect(url_for('course.details', course_id=course_id))
    
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    
    if due_date_str:
        from datetime import datetime
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    else:
        due_date = None
        
    from CampusHub.models.assignment_model import Assignment
    assignment = Assignment(title=title, description=description, due_date=due_date, course_id=course.id)
    db.session.add(assignment)
    db.session.commit()
    
    flash('Assignment created.', 'success')
    return redirect(url_for('course.details', course_id=course_id))
