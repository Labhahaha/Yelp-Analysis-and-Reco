import random

from flask import Blueprint, jsonify, json
from flask import request
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from joblib import load

friends_blue = Blueprint('friends', __name__)

def get_friends_of_friends(user_id):
    with get_session() as session:
        query = text(f"SELECT user_friends From users WHERE user_id = '{user_id}'")
        df = session.execute(query)
        df = toDataFrame(df)
    if df.size == 0:
        return None
    friend_ids = tuple(df['user_friends'][0].split(', '))

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


def get_review_same_business(user_id):
    with get_session() as session:
        query = text(f"SELECT DISTINCT rev_user_id AS user_id FROM review WHERE rev_business_id in \
        (SELECT DISTINCT rev_business_id From review WHERE rev_user_id = '{user_id}') AND rev_user_id != '{user_id}'")
        df = session.execute(query)
        df = toDataFrame(df)
    if df.size == 0:
        return None
    review_same_business = df['user_id'].tolist()
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


def find_candidate_set(user_id):
    friends_of_friends_ids = get_friends_of_friends(user_id)
    print('1')
    review_same_business_ids = get_review_same_business(user_id)
    print('2')
    candidate_set_ids = list(set(friends_of_friends_ids) | set(review_same_business_ids))
    candidate_set_ids = tuple(random.sample(candidate_set_ids, int(len(candidate_set_ids)*0.1)))
    with get_session() as session:
        query = text(f"""
                     SELECT user_id, user_name, user_friends, user_average_stars, user_review_count, user_useful, 
                            user_funny, user_cool, user_fans, user_compliment_hot, user_compliment_more, 
                            user_compliment_profile, user_compliment_cute, user_compliment_list, user_compliment_note, 
                            user_compliment_plain, user_compliment_cool, user_compliment_funny, user_compliment_writer,
                            user_compliment_photos
                     FROM users
                     WHERE user_id in {candidate_set_ids}
                     """)
        df = session.execute(query)
        print('3')
        df = toDataFrame(df)
    df['user_friends_count'] = df['user_friends'].str.count(', ')
    df = df.drop(columns=['user_friends'])
    df['user_average_stars'] = df['user_average_stars'].astype(int)
    return df


def get_user_feature(user_id):
    with get_session() as session:
        query = text(f"""
                             SELECT user_friends, user_average_stars, user_review_count, user_useful, user_funny,
                                    user_cool, user_fans, user_compliment_hot, user_compliment_more, user_compliment_profile,
                                    user_compliment_cute, user_compliment_list, user_compliment_note, user_compliment_plain,
                                    user_compliment_cool, user_compliment_funny, user_compliment_writer,user_compliment_photos
                             FROM users
                             WHERE user_id = '{user_id}'
                             """)
        df = session.execute(query)
        print('4')
        df = toDataFrame(df)

    df['user_friends_count'] = df['user_friends'].str.count(', ')
    df = df.drop(columns=['user_friends'])
    df['user_average_stars'] = df['user_average_stars'].astype(int)
    return df

@friends_blue.route("/recommend_friends")
def recommend_friends():
    user_id = request.args.get("user_id")
    k = 25
    scaler = StandardScaler()
    pca = load(f'config/model/pca10.joblib')
    kmeans = load(f'config/model/kmeans_model{k}.joblib')

    user_X = get_user_feature(user_id)
    scaler.fit(user_X.values)
    user_X_scaled = scaler.fit_transform(user_X.values)
    user_X_pca = pca.transform(user_X_scaled)
    user_cluster_id = kmeans.predict(user_X_pca)[0]

    candidate_set_df = find_candidate_set(user_id)


    candidate_set_X = candidate_set_df.drop(columns=['user_id', 'user_name'])
    scaler.fit(candidate_set_X.values)
    candidate_set_X_scaled = scaler.transform(candidate_set_X.values)
    candidate_set_X_pca = pca.transform(candidate_set_X_scaled)
    cluster_ids = kmeans.predict(candidate_set_X_pca)
    df = candidate_set_df.drop(columns=['user_friends_count', 'user_average_stars', 'user_review_count', 'user_useful',
                                        'user_funny', 'user_cool', 'user_fans', 'user_compliment_hot',
                                        'user_compliment_more', 'user_compliment_profile', 'user_compliment_cute',
                                        'user_compliment_list', 'user_compliment_note', 'user_compliment_plain',
                                        'user_compliment_cool', 'user_compliment_funny', 'user_compliment_writer',
                                        'user_compliment_photos'])
    df['cluster_id'] = cluster_ids
    distances = []
    for idx, cluster in enumerate(cluster_ids):
        if cluster == user_cluster_id:
            distance = euclidean(user_X_pca[0], candidate_set_X_pca[idx])
            distances.append((idx, distance))

    # 根据距离找到距离最近的10个数据点
    distances.sort(key=lambda x: x[1])  # 按距离升序排序

    count = 10
    nearest = distances[:min(count, len(cluster_ids))]  # 获取前10个距离最近的数据点的索引和距离
    nearest_list = []
    for n in nearest:
        nearest_list.append(n[0])
    # 提取距离最近的10个数据点
    candidate_set_df = candidate_set_df[['user_id', 'user_name']]
    nearest_data = candidate_set_df.loc[nearest_list]
    return json.dumps(nearest_data.to_dict(orient='records'))









