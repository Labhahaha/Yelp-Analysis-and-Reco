from flask import Blueprint, request, json
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from ..utils.get_distance import cal_distance

recommend_blue = Blueprint('recommend_blue', __name__)

business_df = None

@recommend_blue.route('/recommend')
def get_recommendations():
    global business_df
    user_location = json.loads(request.args.get('user_location'))
    user_id = request.args.get('user_id')
    city = request.args.get('city')
    if business_df is None:
        business_df = get_business_by_city(city)
    get_distance_for_business(user_location)
    get_score_for_business(user_id)


    return 'Hello World!'

def get_score_for_business(user_id):
    global business_df
    business_df['score'] = business_df['stars']

def get_distance_for_business(user_location):
    global business_df
    business_df['distance'] = business_df.apply(
        lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]), axis=1)

def get_business_by_city(city):
    with get_session() as session:
        query = text(f"select * from business where city = '{city}'")
        res = session.execute(query)
        res = toDataFrame(res)
        return res
