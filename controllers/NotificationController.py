import smtplib
from email.mime.text import MIMEText

def SendEmail(Title, Content):
    try:
        Sender = "your-email@example.com"
        Reciver = "student@example.com"  # In Phase 5: loop through all students

        msg = MIMEText(Content)
        msg["Subject"] = f"New Announcement: {Title}"
        msg["From"] = Sender
        msg["To"] = Reciver

        # Gmail SMTP example
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(Sender, "your-app-password")
            server.sendmail(Sender, Reciver, msg.as_string())

    except Exception as e:
        print("Email sending failed:", e)
