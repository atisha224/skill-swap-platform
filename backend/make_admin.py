from app import app, db
from models import User

# Replace this with the email of the user you want to make admin
target_email = "admin@example.com"

with app.app_context():
    user = User.query.filter_by(email=target_email).first()

    if user:
        user.role = "admin"
        db.session.commit()
        print(f"{user.name} is now an admin.")
    else:
        print("User not found.")
