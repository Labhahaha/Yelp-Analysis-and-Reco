import pandas as pd
from flask import Blueprint, request, json, jsonify
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from ..utils import get_business_by_city
from .CollaborativeFiltering import CollaborativeFiltering
from .QueryBased import match_rating
from .LocationBased import location_based_list

recommend_blue = Blueprint('recommend_blue', __name__)

business_df = None
review_df = None
city = None


@recommend_blue.route('/recommend')
def get_recommendations():
    global business_df, review_df, city
    user_location = json.loads(request.args.get('user_location'))
    user_id = request.args.get('user_id')
    query = request.args.get('query')
    res = request.args.get('city')
    if (city is None) or (res != city):
        if res is None:
            return 'city not found', 400
        city = res
        business_df = get_business_by_city(city)
        review_df = get_review_by_business(tuple(business_df['business_id'].values))

    if query is not None:
        candidate_set3 = get_query_based_candidate_set(query, business_df, 20)
        print(candidate_set3)

    if user_id is not None:
        candidate_set1 = get_collaborative_filtering_candidate_set(user_id, business_df,20)
        print(candidate_set1)

    if user_location is not None:
        candidate_set2 = get_location_based_candidate_set(user_location, business_df, 1)
        print(candidate_set2)

    candidate_set4 = get_alternate_set(business_df, 20)
    print(candidate_set4)



    # fused_candidate = fuse_candidate_set(candidate_set1,candidate_set2,candidate_set3,candidate_set4)

    # recommend_list = re_sort(fused_candidate)

    # recommend_list_withInfo = add_Info(recommend_list)

    return business_df.to_json(orient='records')


def get_collaborative_filtering_candidate_set(user_id, business_df, k):
    rating_list = CollaborativeFiltering(user_id, pd.DataFrame(business_df['business_id']))
    rating_list = pd.merge(business_df, rating_list, left_on='business_id', right_on='business_id')
    top_k_recommendations = rating_list.sort_values(by='rating', ascending=False).head(k)
    return top_k_recommendations[['business_id', 'name', 'rating']]


def get_location_based_candidate_set(user_location, business_df, k):
    top_k_recommendations = location_based_list(user_location, business_df, k)
    return top_k_recommendations[['business_id', 'name', 'district','distance']]


def get_query_based_candidate_set(query, business_df, k):
    business_texts = pd.DataFrame({'business_text': "The name of this business is " + business_df[
        'name'] + ' and its categories include ' + business_df['categories']})
    rating_list = match_rating(query, business_texts)
    rating_list = pd.concat([business_df, rating_list], axis=1)
    top_k_recommendations = rating_list.sort_values(by='match_rating', ascending=False).head(k)
    return top_k_recommendations[['business_id', 'name', 'match_rating']]


def get_alternate_set(business_df, k):
    # 归一化评分和评价数量列
    normalized_stars = (business_df['stars'] - business_df['stars'].min()) / (
                business_df['stars'].max() - business_df['stars'].min())
    normalized_review_count = (business_df['review_count'] - business_df['review_count'].min()) / (
                business_df['review_count'].max() - business_df['review_count'].min())
    # 计算加权得分，假设评分占比为 0.7，评价数量占比为 0.3
    weighted_score = 0.7 * normalized_stars + 0.3 * normalized_review_count
    # 添加加权得分列
    business_df['weighted_score'] = weighted_score
    # 根据加权得分降序排序，选择前 k 个商家作为候选集
    top_k_recommendations = business_df.sort_values(by='weighted_score', ascending=False).head(k)
    return top_k_recommendations[['business_id', 'name', 'weighted_score']]

def fuse_candidate_set(candidate_set1, candidate_set2, candidate_set3, candidate_set4):
    pass


def re_sort(fused_candidate):
    pass


def add_Info(recommend_list):
    pass


def get_review_by_business(business):
    with get_session() as session:
        query = text(f"select * from review where rev_business_id in {business}")
        res = session.execute(query)
        res = toDataFrame(res)
        return res


@recommend_blue.route('/details')
def getBusinessDetails():
    business_id = request.args.get('business_id')
    res = {
        'business': business_df[business_df['business_id'] == business_id].to_dict(orient='records')[0],
        'review': review_df[review_df['rev_business_id'] == business_id].to_dict(orient='records'),
    }
    res = jsonify(res)
    return res
