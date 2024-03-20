import random
from flask import Blueprint, jsonify, json
from flask import request
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from ..Recommendation import Recommend
from joblib import load

friends_blue = Blueprint('friends', __name__)


# 得到好友的好友，作为候选集的一部分
def get_friends_of_friends(user_id):
    # 得到用户的好友，并转成元组
    with get_session() as session:
        query = text(f"SELECT user_friends From users WHERE user_id = '{user_id}'")
        df = session.execute(query)
        df = toDataFrame(df)
        if df['user_friends'][0]=='None':return []

    friend_ids = tuple(df['user_friends'][0].split(', '))

    # 得到好友的好友
    friend_of_friend_ids = []
    with get_session() as session:
        query = text(f"SELECT user_friends From users WHERE user_id in {friend_ids}")
        friend_df = session.execute(query)
        friend_df = toDataFrame(friend_df)
    for row in friend_df['user_friends']:
        ids = row.split(', ')
        friend_of_friend_ids.extend(ids)

    # 去重并排除已经是好友的用户
    result = list(set(friend_of_friend_ids) - set(friend_ids))
    return result


# 得到评论过同一家店的用户，作为候选集的一部分
def get_review_same_business(user_id):
    # 查询评论过同一家店的用户
    with get_session() as session:
        query = text(f"SELECT DISTINCT rev_user_id AS user_id FROM review WHERE rev_business_id in \
        (SELECT DISTINCT rev_business_id From review WHERE rev_user_id = '{user_id}') AND rev_user_id != '{user_id}'")
        df = session.execute(query)
        df = toDataFrame(df)
    if df.size == 0:
        return []
    review_same_business = df['user_id'].tolist()

    # 查询用户的好友
    with get_session() as session:
        query = text(f"SELECT user_friends From users WHERE user_id = '{user_id}'")
        df = session.execute(query)
        df = toDataFrame(df)
    if df.size == 0:
        return None
    friend_ids = df['user_friends'][0].split(', ')

    # 去重并排除已经是好友的用户
    result = list(set(review_same_business) - set(friend_ids))
    return result


# 得到候选集（好友的好友和评论过同一家店的用户的并集）
def find_candidate_set(user_id):
    # 得到候选集的id
    friends_of_friends_ids = get_friends_of_friends(user_id)
    review_same_business_ids = get_review_same_business(user_id)
    candidate_set_ids = list(set(friends_of_friends_ids) | set(review_same_business_ids))
    candidate_set_ids = tuple(random.sample(candidate_set_ids, min(1000,len(candidate_set_ids))))
    # 得到候选集
    with get_session() as session:
        query = text(f"SELECT * FROM users WHERE user_id in {candidate_set_ids}")
        df = session.execute(query)
        df = toDataFrame(df)
    df['user_friends_count'] = df['user_friends'].str.count(', ')
    df['user_average_stars'] = df['user_average_stars'].astype(int)
    return df


# 得到用户的信息
def get_user_feature(user_id):
    with get_session() as session:
        query = text(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        df = session.execute(query)
        df = toDataFrame(df)
    df['user_friends_count'] = df['user_friends'].str.count(', ')
    df['user_average_stars'] = df['user_average_stars'].astype(int)
    return df


# 推荐好友
@friends_blue.route("/recommend_friends")
def recommend_friends():
    user_id = request.args.get("user_id")
    k = 25
    user_id = Recommend.user_id
    # 归一化、主成分分析和kmeans
    scaler = StandardScaler()
    pca = load(f'config/model/PCA/pca10.joblib')
    kmeans = load(f'config/model/K-means/kmeans_model{k}.joblib')

    # 模型预测需要输入的特征参数
    features_column = ['user_friends_count', 'user_average_stars', 'user_review_count', 'user_useful', 'user_funny',
                       'user_cool', 'user_fans', 'user_compliment_hot', 'user_compliment_more', 'user_compliment_profile',
                       'user_compliment_cute', 'user_compliment_list', 'user_compliment_note', 'user_compliment_plain',
                       'user_compliment_cool', 'user_compliment_funny', 'user_compliment_writer', 'user_compliment_photos']

    # 预测候选集
    candidate_set_df = find_candidate_set(user_id)
    candidate_set_feature_scaled = scaler.fit_transform(candidate_set_df[features_column])
    candidate_set_feature_pca = pca.transform(candidate_set_feature_scaled)
    cluster_ids = kmeans.predict(candidate_set_feature_pca)

    # 预测登录用户
    user = get_user_feature(user_id)
    user_feature_scaled = scaler.transform(user[features_column])
    user_feature_pca = pca.transform(user_feature_scaled)
    user_cluster_id = kmeans.predict(user_feature_pca)[0]

    # 计算用户与候选集中在同一个簇中的数据点的欧氏距离
    distances = []
    for idx, cluster in enumerate(cluster_ids):
        if cluster == user_cluster_id:
            distance = euclidean(user_feature_pca[0], candidate_set_feature_pca[idx])
            distances.append((idx, distance))
    # 根据距离找到距离最近的10个数据点
    distances.sort(key=lambda x: x[1])  # 按距离升序排序
    count = 36
    nearest = distances[:min(count, len(cluster_ids))]  # 获取前10个距离最近的数据点的索引和距离
    nearest_list = []
    for n in nearest:
        nearest_list.append(n[0])

    # 提取距离最近的10个数据点
    nearest_data = candidate_set_df.loc[nearest_list]
    return json.dumps(nearest_data.to_dict(orient='records'))









