from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    profile_photo = db.Column(db.String(120))  # path or filename
    skills_offered = db.Column(db.String(300))
    skills_wanted = db.Column(db.String(300))
    availability = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default='user')  # 'user' or 'admin'
    is_banned = db.Column(db.Boolean, default=False)

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, nullable=False)
    to_user_id = db.Column(db.Integer, nullable=False)
    offered_skill = db.Column(db.String(100), nullable=False)
    wanted_skill = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, deleted
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, nullable=False)
    to_user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
