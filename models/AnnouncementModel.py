from database import DbConnection

class AnnouncementModel:

    def create_announcement(self, title, content, instructor_id):
        conn = DbConnection()
        cursor = conn.cursor()

        query = "INSERT INTO announcements (title, content, instructor_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, content, instructor_id))

        conn.commit()
        conn.close()


    def get_all_announcements(self):
        conn = DbConnection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM announcements ORDER BY created_at DESC"
        cursor.execute(query)

        rows = cursor.fetchall()
        conn.close()
        return rows
