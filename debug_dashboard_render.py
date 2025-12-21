from CampusHub.app import create_app
from CampusHub.models.feedback_model import Feedback
from CampusHub.models.user_model import User
from flask import render_template
from CampusHub.extensions import db

app = create_app()
app.config['SERVER_NAME'] = 'localhost' 
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    # 1. Check Data
    count = Feedback.query.count()
    print(f"Feedback Count in DB: {count}")
    
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    print(f"Feedback Objects: {feedbacks}")
    
    if not feedbacks:
        print("Creating dummy feedback...")
        u = User.query.first()
        if not u:
            u = User(email='admin@debug.com', role='admin')
            db.session.add(u)
            db.session.commit()
            
        f = Feedback(user_id=u.id, message='MAGIC_STRING_DEBUG', category='Bug')
        db.session.add(f)
        db.session.commit()
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
        print(f"Feedback Objects after creation: {feedbacks}")

    # 2. Render Template
    with app.test_request_context('/admin/dashboard'):
        from flask_login import login_user
        u = User.query.first()
        login_user(u)
        
        try:
            output = render_template('admin/dashboard.html', 
                                   total_users=10, 
                                   total_events=5, 
                                   pending_events=2, 
                                   total_feedbacks=len(feedbacks), 
                                   feedbacks=feedbacks)
            
            if "MAGIC_STRING_DEBUG" in output or (feedbacks and feedbacks[0].message in output):
                print("SUCCESS: Feedback message found in rendered HTML.")
            else:
                print("FAILURE: Feedback message NOT found in rendered HTML.")
                start = output.find("Recent Feedback")
                if start != -1:
                    print("--- Table Snippet ---")
                    print(output[start:start+1000])
                    print("---------------------")
        except Exception as e:
            print(f"Rendering Exception: {e}")
