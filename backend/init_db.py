from app import app, db  # Make sure these are correctly imported

with app.app_context():
    db.create_all()
    print("Database updated with new tables.")
