from flask import Blueprint, jsonify, request
from .models import get_users, create_user, get_businesses, create_business, get_reviews, create_review, get_checkins, \
    create_checkin

api_bp = Blueprint('api', __name__)


@api_bp.route('/users', methods=['GET'])
def get_users_route():
    users_df = get_users()
    users = users_df.toJSON().collect()
    return jsonify(users), 200


@api_bp.route('/users', methods=['POST'])
def create_user_route():
    user_data = request.get_json()
    create_user(user_data)
    return jsonify({"message": "User created successfully"}), 201

# 添加其他路由和视图函数...
