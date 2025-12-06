from flask import Flask
from controllers.AnnouncementController import create_announcement, list_announcements

app = Flask(__name__)
app.secret_key = "secret-phase4"  # Required for session


app.add_url_rule('/announcement/create', view_func=create_announcement, methods=['GET', 'POST'])
app.add_url_rule('/announcements', view_func=list_announcements, methods=['GET'])
