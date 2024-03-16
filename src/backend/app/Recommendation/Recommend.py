import pandas as pd
from flask import Blueprint, request, json, jsonify
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from ..utils import get_business_by_city, cal_distance, location_init
from .CollaborativeFiltering import CollaborativeFiltering
from .QueryBased import match_rating
from .LocationBased import location_based_list
from ..Advice.Sentiment import sentiment_predict

# 创建路由蓝图
recommend_blue = Blueprint('recommend_blue', __name__)
# 城市商家和评论dataframe
business_df = None
review_df = None
# 基本变量信息
city = 'Abington'
last_city = None
user_location = None
user_id = None


@recommend_blue.route('/')
def get_recommendations(p_query=None):
    global business_df, review_df, city, last_city, user_location, user_id
    # 获取请求参数
    p_user_id = request.args.get('user_id')
    p_city = request.args.get('city')
    p_user_location = request.args.get('user_location')
    # 更新查询参数
    query = request.args.get('query')
    if p_user_id is not None:
        query = p_query

    # 更新其它参数
    if p_user_id is not None:
        user_id = p_user_id
    if p_user_location is not None:
        p_user_location = json.loads(p_user_location)
        user_location = p_user_location
    if p_city is not None:
        city = p_city

    # 更新城市信息，重新拉取城市商户和评论信息
    if city != last_city:
        last_city = city
        business_df = get_business_by_city(city)
        user_location = location_init(business_df)
        review_df = get_review_by_business(tuple(business_df['business_id'].values))

    # 基于查询的推荐
    if query is not None:
        query_candidate_set = get_query_based_candidate_set(query, business_df, 72)
    else:
        query_candidate_set = None

    # 基于协同过滤的推荐
    if user_id is not None:
        collaborative_candidate_set = get_collaborative_filtering_candidate_set(user_id, business_df, 72)
    else:
        collaborative_candidate_set = None

    # 基于用户位置的推荐
    if user_location is not None:
        location_candidate_set = get_location_based_candidate_set(user_location, business_df, 72)
    else:
        location_candidate_set = None

    # 基于评价和单量的候选集的推荐
    alternate_candidate_set = get_alternate_set(business_df, 72)

    # 候选集融合和过滤
    fused_candidate = fuse_candidate_set(collaborative_candidate_set, location_candidate_set, query_candidate_set,
                                         alternate_candidate_set, 72)

    # 候选集重排序得到推荐集
    recommend_list = re_sort(fused_candidate)

    # 完善推荐集的详细信息
    recommend_list_with_info = add_Info(recommend_list, business_df)

    return recommend_list_with_info.to_json(orient='records')


# 根据用户ID和城市商户情况使用协同过滤的方法获得候选集
def get_collaborative_filtering_candidate_set(user_id, business_df, k):
    # 使用协同过滤模型获得评分列表
    rating_list = CollaborativeFiltering(user_id, pd.DataFrame(business_df['business_id']))
    rating_list = pd.merge(business_df, rating_list, left_on='business_id', right_on='business_id')
    # 筛选高分topK进行推荐
    rating_list = rating_list[rating_list['rating'] > 4.0]
    top_k_recommendations = rating_list.sort_values(by='rating', ascending=False).head(k)
    print(top_k_recommendations[['business_id', 'name', 'rating']])
    return top_k_recommendations['business_id']


# 根据用户位置和城市商户情况使用基于位置的方法获得候选集
def get_location_based_candidate_set(user_location, business_df, k):
    # 使用基于位置算法获得推荐列表
    top_k_recommendations = location_based_list(user_location, business_df, k)
    print(top_k_recommendations[['business_id', 'name', 'district', 'distance']])
    if top_k_recommendations.empty:
        return None
    return top_k_recommendations['business_id']


# 根据用户查询文本使用NLP分析方法获得候选集
def get_query_based_candidate_set(query, business_df, k):
    # 通过用户查询文本和城市商户信息生成文本提示
    business_texts = pd.DataFrame({'business_text': "The name of this business is " + business_df[
        'name'] + ' and its categories include ' + business_df['categories']})
    # 通过文本匹配模型获得匹配分数
    rating_list = match_rating(query, business_texts)
    rating_list = pd.concat([business_df, rating_list], axis=1)
    # 筛选高匹配分数topK进行推荐
    top_k_recommendations = rating_list.sort_values(by='match_rating', ascending=False).head(k)
    print(top_k_recommendations[['business_id', 'name', 'match_rating']])
    return top_k_recommendations['business_id']


# 根据城市商户情况获得替补候选集
def get_alternate_set(business_df, k):
    # 归一化评分和评价数量列
    normalized_stars = (business_df['stars'] - business_df['stars'].min()) / (
            business_df['stars'].max() - business_df['stars'].min())
    normalized_review_count = (business_df['review_count'] - business_df['review_count'].min()) / (
            business_df['review_count'].max() - business_df['review_count'].min())
    # 计算加权得分，假设评分占比为 0.7，评价数量占比为 0.3
    weighted_score = 0.7 * normalized_stars + 0.3 * normalized_review_count
    business_df = business_df.copy()
    # 添加加权得分列
    business_df['weighted_score'] = weighted_score
    # 根据加权得分降序排序，选择前 k 个商家作为候选集
    top_k_recommendations = business_df.sort_values(by='weighted_score', ascending=False).head(k)
    print(top_k_recommendations[['business_id', 'name', 'weighted_score']])
    return top_k_recommendations['business_id']


# 候选集融合和过滤
def fuse_candidate_set(collaborative_candidate_set, location_candidate_set, query_candidate_set,
                       alternate_candidate_set, k=72):
    # 若有查询结果则查询优先级最高，直接返回基于查询的候选集
    if query_candidate_set is not None:
        res = query_candidate_set
        return res
    # 若无查询，则根据剩余策略进行融合推荐
    # 若有user_id
    elif collaborative_candidate_set is not None:
        # 优先使用协同过滤模型进行推荐
        res = collaborative_candidate_set
        # 若高分推荐数量不足
        if res.shape[0] < k:
            if location_candidate_set is not None:
                # 使用基于位置推荐进行递补推荐
                res = pd.concat([res, location_candidate_set.head(k - res.shape[0])], axis=0)
            if res.shape[0] < k:
                # 使用替补集进行递补推荐
                res = pd.concat([res, alternate_candidate_set.head(k - res.shape[0])], axis=0)
        return res
    # 若无user_id, 则根据剩余策略进行融合推荐
    elif location_candidate_set is not None:
        # 优先使用基于位置的算法进行推荐
        res = location_candidate_set
        # 基于位置推荐数量不足
        if res.shape[0] < k:
            # 使用替补集进行递补推荐
            res = pd.concat([res, alternate_candidate_set.head(k - res.shape[0])], axis=0)
        return res
    # 若无user_id与用户位置,则使用替补集进行推荐
    elif alternate_candidate_set is not None:
        res = alternate_candidate_set
        return res
    else:
        return None


# 候选集重排序
def re_sort(fused_candidate):
    return fused_candidate


# 根据business_id列表匹配详细信息
def add_Info(fused_candidate, business_df):
    global user_location
    res = pd.merge(fused_candidate, business_df, how='left', on='business_id')
    if user_location is not None:
        res['distance'] = res.apply(lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]),
                                    axis=1)
    return res


def get_review_by_business(business):
    with get_session() as session:
        query = text(f"select * from review where rev_business_id in {business}")
        res = session.execute(query)
        res = toDataFrame(res)
        return res


# 根据business_id返回商户详细信息
@recommend_blue.route('/details')
def getBusinessDetails():
    business_id = request.args.get('business_id')
    tmp_business_df = business_df[business_df['business_id'] == business_id]
    tmp_review_df = review_df[review_df['rev_business_id'] == business_id]
    tmp_review_df = tmp_review_df.reset_index(drop=True)
    texts = tmp_review_df['rev_text'].values.tolist()
    sentiments = sentiment_predict(texts)[['sentiment', 'predicted_probability']]
    tmp_review_df = pd.concat([tmp_review_df, sentiments], axis=1)
    res = {
        'business': tmp_business_df.to_dict(orient='records')[0],
        'review': tmp_review_df.to_dict(orient='records'),
    }
    res = jsonify(res)
    return res
