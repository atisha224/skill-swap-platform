from app import app, db  # Make sure this works. Adjust if needed.

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
