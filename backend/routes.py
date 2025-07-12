from flask import Blueprint, request, jsonify
from models import User, SwapRequest, Feedback
from extensions import db  # ✅ not from app
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from flask import Response

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    name = data.get('name')

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already exists"}), 400

    user = User(email=email, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True, "message": "User registered successfully"})

@api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    return jsonify({
        "success": True,
        "user_id": user.id,
        "name": user.name,
        "is_admin": user.role == 'admin'
    })


@api_bp.route('/api/profile/update', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user.name = data.get('name', user.name)
    user.location = data.get('location', user.location)
    user.skills_offered = data.get('skills_offered', user.skills_offered)
    user.skills_wanted = data.get('skills_wanted', user.skills_wanted)
    user.availability = data.get('availability', user.availability)
    user.is_public = data.get('is_public', user.is_public)

    db.session.commit()

    return jsonify({"success": True, "message": "Profile updated"})


@api_bp.route('/api/public-profiles', methods=['GET'])
def public_profiles():
    skill = request.args.get('skill', '').lower()

    users = User.query.filter_by(is_public=True).all()
    result = []

    for user in users:
        if user.skills_offered and skill in user.skills_offered.lower():
            result.append({
                "id": user.id,
                "name": user.name,
                "location": user.location,
                "skills_offered": user.skills_offered,
                "skills_wanted": user.skills_wanted,
                "availability": user.availability
            })

    return jsonify({"success": True, "users": result})


@api_bp.route('/api/request-swap', methods=['POST'])
def request_swap():
    data = request.get_json()
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    offered_skill = data.get('offered_skill')
    wanted_skill = data.get('wanted_skill')

    # Prevent users from requesting themselves
    if from_user_id == to_user_id:
        return jsonify({"success": False, "message": "Cannot request your own profile"}), 400

    # Check if a similar request already exists
    existing = SwapRequest.query.filter_by(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        status='pending'
    ).first()

    if existing:
        return jsonify({"success": False, "message": "Swap request already pending"}), 400

    swap = SwapRequest(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        offered_skill=offered_skill,
        wanted_skill=wanted_skill
    )

    db.session.add(swap)
    db.session.commit()

    return jsonify({"success": True, "message": "Swap request sent!"})


@api_bp.route('/api/swap-requests/<int:user_id>', methods=['GET'])
def get_swap_requests(user_id):
    sent = SwapRequest.query.filter_by(from_user_id=user_id).all()
    received = SwapRequest.query.filter_by(to_user_id=user_id).all()

    def format_request(r):
        return {
            "id": r.id,
            "from_user_id": r.from_user_id,
            "to_user_id": r.to_user_id,
            "offered_skill": r.offered_skill,
            "wanted_skill": r.wanted_skill,
            "status": r.status,
            "timestamp": r.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

    return jsonify({
        "success": True,
        "sent_requests": [format_request(r) for r in sent],
        "received_requests": [format_request(r) for r in received]
    })


@api_bp.route('/api/swap-request/<int:request_id>', methods=['POST'])
def update_swap_status(request_id):
    data = request.get_json()
    new_status = data.get('status')  # 'accepted', 'rejected', 'deleted'

    if new_status not in ['accepted', 'rejected', 'deleted']:
        return jsonify({"success": False, "message": "Invalid status value"}), 400

    request_obj = SwapRequest.query.get(request_id)
    if not request_obj:
        return jsonify({"success": False, "message": "Swap request not found"}), 404

    request_obj.status = new_status
    db.session.commit()

    return jsonify({"success": True, "message": f"Request {new_status}"})


@api_bp.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback = Feedback(
        from_user_id=data.get('from_user_id'),
        to_user_id=data.get('to_user_id'),
        rating=data.get('rating'),
        message=data.get('message')
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"success": True, "message": "Feedback submitted"})


@api_bp.route('/api/feedback/<int:user_id>', methods=['GET'])
def get_feedback(user_id):
    feedbacks = Feedback.query.filter_by(to_user_id=user_id).all()
    result = [{
        "from_user_id": fb.from_user_id,
        "rating": fb.rating,
        "message": fb.message,
        "timestamp": fb.timestamp
    } for fb in feedbacks]

    return jsonify({"success": True, "feedback": result})


@api_bp.route('/api/admin/ban-user/<int:user_id>', methods=['POST'])
def ban_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user.is_banned = True
    db.session.commit()
    return jsonify({"success": True, "message": "User banned"})


@api_bp.route('/api/admin/stats', methods=['GET'])
def get_stats():
    users = User.query.count()
    swaps = SwapRequest.query.count()
    feedbacks = Feedback.query.count()

    return jsonify({
        "total_users": users,
        "total_swaps": swaps,
        "total_feedback": feedbacks
    })


@api_bp.route('/api/admin/export-feedback', methods=['GET'])
def export_feedback():
    feedbacks = Feedback.query.all()

    def generate():
        data = csv.writer()
        yield ','.join(["from_user_id", "to_user_id", "rating", "message", "timestamp"]) + '\n'
        for f in feedbacks:
            row = [str(f.from_user_id), str(f.to_user_id), str(f.rating), f.message, f.timestamp.isoformat()]
            yield ','.join(row) + '\n'

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=feedback_logs.csv"})
