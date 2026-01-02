from app import create_app
from app.db import get_db
from download import filename_from_url
import sqlite3

def updatedb():
    app = create_app()

    with app.app_context():
        db = get_db()

        # 1. Add column if it doesn't exist
        try:
            db.execute("ALTER TABLE all_questions ADD COLUMN image_title TEXT")
        except sqlite3.OperationalError:
            pass  # column already exists

        # 2. Copy existing image into image_url
        db.execute("UPDATE all_questions SET image_url = image")

        # 3. Fetch rows properly
        rows = db.execute(
            "SELECT id, image_url FROM all_questions WHERE image_url IS NOT NULL"
        ).fetchall()

        # 4. Update each row safely
        for row in rows:
            filename = filename_from_url(row["image_url"])
            db.execute(
                "UPDATE all_questions SET image = ? WHERE id = ?",
                (filename, row["id"])
            )

        db.commit()
