from flask import Blueprint, request,json
from ..utils import get_distance
recommend_blue = Blueprint('recommend_blue', __name__)

@recommend_blue.route('/')
def get_recommendations():
    position = json.loads(request.args.get('position'))
    user_id = request.args.get('user_id')
    city = request.args.get('city')

    return 'Hello World!'