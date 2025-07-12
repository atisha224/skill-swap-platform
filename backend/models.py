from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    location = db.Column(db.String(100))
    profile_photo = db.Column(db.String(200))
    skills_offered = db.Column(db.String(300))
    skills_wanted = db.Column(db.String(300))
    availability = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(10), default='user')
    is_banned = db.Column(db.Boolean, default=False)

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer)
    to_user_id = db.Column(db.Integer)
    offered_skill = db.Column
