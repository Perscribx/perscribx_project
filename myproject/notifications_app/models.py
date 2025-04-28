from django.db import models
import sqlite3

class SummaryEntry(models.Model):
    def __init__(self, db_name="notifications.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            date TEXT,
            text TEXT,
            pdf_url TEXT,
            url TEXT,
            priority INTEGER,
            summary_pl TEXT,
            summary_en TEXT,
            summary_it TEXT,
            summary_de TEXT,
            summary_fr TEXT,
            summary_es TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def check_record_by(data):
        entries = SummaryEntry.objects.filter(data__date=data)
        
        if entries.exists():
            for entry in entries:
                return True

        else:
            return False

    def add_notification(self, title, author, text, summarised_text=None, pdf_url=None, url=None, priority=0,
                         date=None):

        query = """
          INSERT INTO notifications (title, author, date, text, summarised_text,, pdf_url, url, priority)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
          """
        self.conn.execute(query, (title, author, date, text, summarised_text, pdf_url, url, priority))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def update_field(self, title, field, value):
        allowed_fields = [
            "title", "author", "date", "text", "summarised_text",
            "pdf_url", "url", "priority",
            "summary_pl", "summary_en", "summary_it",
            "summary_de", "summary_fr", "summary_es"
        ]

        if field not in allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed to be updated.")

        query = f"UPDATE notifications SET {field} = ? WHERE title = ?"
        self.conn.execute(query, (value, title))
        self.conn.commit()

    def check_if_exists(self, field, value):
        allowed_fields = [
            "title", "author", "date", "text", "summarised_text",
            "pdf_url", "url", "priority",
            "summary_pl", "summary_en", "summary_it",
            "summary_de", "summary_fr", "summary_es"
        ]

        if field not in allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed for checking.")

        query = f"SELECT 1 FROM notifications WHERE {field} = ? LIMIT 1"
        cursor = self.conn.execute(query, (value,))
        result = cursor.fetchone()

        return result is not None