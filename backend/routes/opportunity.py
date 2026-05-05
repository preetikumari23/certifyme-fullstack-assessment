from flask import Blueprint, request, jsonify, session
from models import db, Opportunity

opp_bp = Blueprint('opp', __name__)

def get_admin():
    return session.get('admin_id')

@opp_bp.route('/opportunities', methods=['GET'])
def get_all():
    admin_id = get_admin()
    if not admin_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = Opportunity.query.filter_by(admin_id=admin_id).all()

    return jsonify([{
        "id": o.id,
        "name": o.name,
        "duration": o.duration,
        "start_date": o.start_date,
        "description": o.description,
        "skills": o.skills,
        "category": o.category,
        "future_opportunities": o.future_opportunities,
        "max_applicants": o.max_applicants
    } for o in data])