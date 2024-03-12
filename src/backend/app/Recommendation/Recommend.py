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
    # 获取推荐所需参数
    user_location = json.loads(request.args.get('user_location'))
    user_id = request.args.get('user_id')
    city = request.args.get('city')
    query = request.args.get('query')
    # 初始化该城市dataframe信息
    if business_df is None:
        business_df = get_business_by_city(city)
    if review_df is None:
        review_df = get_review_by_business(tuple(business_df['business_id'].values))

    #协同过滤算法候选集
    candidate_set1 = get_collaborative_filtering_candidate_set(user_id,business_df['business_id'])
    #基于位置的候选集
    candidate_set2 = get_location_based_candidate_set(user_location)
    #基于查询的候选集
    candidate_set3 = get_query_based_candidate_set(query)
    #基于热点的替补集
    candidate_set4 = get_alternate_set(user_location)

    #候选集融合
    fused_candidate = fuse_candidate_set(candidate_set1,candidate_set2,candidate_set3,candidate_set4)

    #候选集重排序
    recommend_list = re_sort(fused_candidate)

    #加载推荐列表相关信息
    recommend_list_withInfo = add_Info(recommend_list)

    return business_df.to_json(orient='records')


def get_collaborative_filtering_candidate_set(user_id, business_ids):
    pass

def get_location_based_candidate_set(user_location):
    pass

def get_query_based_candidate_set(query):
    pass

def get_alternate_set(user_location):
    pass

def fuse_candidate_set(candidate_set1, candidate_set2, candidate_set3, candidate_set4):
    pass
def re_sort(fused_candidate):
    pass
def add_Info(recommend_list):
    pass

def get_business_by_city(city):
    with get_session() as session:
        query = text(f"select * from business where city = '{city}'")
        res = session.execute(query)
        res = toDataFrame(res)
        return res
def get_review_by_business(business):
    with get_session() as session:
        query = text(f"select * from review where rev_business_id in {business}")
        res = session.execute(query)
        res = toDataFrame(res)
        return res

def get_distance_for_business(user_location):
    global business_df
    business_df['distance'] = business_df.apply(
        lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]), axis=1)


@recommend_blue.route('/details')
def getBusinessDetails():
    business_id = request.args.get('business_id')
    res = {
        'business': business_df[business_df['business_id'] == business_id].to_dict(orient='records')[0],
        'review': review_df[review_df['rev_business_id'] == business_id].to_dict(orient='records'),
    }
    res = jsonify(res)
    return res

