from flask import Blueprint, request,json
from ..utils import get_distance
recommend_blue = Blueprint('recommend_blue', __name__)


# 得到用户与一组商家的距离
def get_distance_by_location(user_location, business_location_list):
    distances = []
    for business_location in business_location_list:
        distance = get_distance(user_location, business_location)
        distances.append(distance)
    return distances




@recommend_blue.route('/')
def get_recommendations():
    position = json.loads(request.args.get('position'))
    user_id = request.args.get('user_id')
    city = request.args.get('city')

    return 'Hello World!'