import pandas as pd
from flask import Blueprint, request, json, jsonify
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from ..utils.get_distance import cal_distance

recommend_blue = Blueprint('recommend_blue', __name__)

business_df = None
review_df = None
@recommend_blue.route('/recommend')
def get_recommendations():
    global business_df,review_df
    user_location = json.loads(request.args.get('user_location'))
    user_id = request.args.get('user_id')
    city = request.args.get('city')
    if business_df is None:
        business_df = get_business_by_city(city)
    if review_df is None:
        review_df = get_review_by_business(tuple(business_df['business_id'].values))

    get_distance_for_business(user_location)
    get_score_for_business(user_id)
    return business_df.to_json(orient='records')


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
def get_review_by_business(business):
    with get_session() as session:
        query = text(f"select * from review where rev_business_id ='JmzNw0WCPmZPZdq5nx9brg'")
        res = session.execute(query)
        res = toDataFrame(res)
        return res

@recommend_blue.route('/detail')
def getBusinessDetails():
    global business_df,review_df
    business_id = request.args.get('business_id')
    res = {
        'business': business_df[business_df['business_id'] == business_id].to_dict(orient='records'),
        'review': review_df[review_df['rev_business_id'] == business_id].to_dict(orient='records'),
    }
    res = jsonify(res)
    return res


