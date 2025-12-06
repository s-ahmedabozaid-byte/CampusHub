from flask import request, render_template, redirect, session
from models.AnnouncementModel import AnnouncementModel

announcement_model = AnnouncementModel()

def create_announcement():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        instructor_id = session.get("user_id", 1)  # TEMP for Phase 4

        announcement_model.create_announcement(title, content, instructor_id)
        return redirect("/announcements")

    return render_template("AnnouncementCreate.html")


def list_announcements():
    announcements = announcement_model.get_all_announcements()
    return render_template("Announcements.html", announcements=announcements)
