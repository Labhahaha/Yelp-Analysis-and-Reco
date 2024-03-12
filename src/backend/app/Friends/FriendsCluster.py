import joblib
import numpy as np
from sqlalchemy import text
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.backend.app.DataAnalyse.SQLSession import (get_session, toJSON, toDataFrame, db_init)
from src.backend.config import config
import pandas as pd
from datetime import datetime
from joblib import dump, load
import random


def userClassification():
    with get_session() as session:
        query = text(f"select user_id, user_review_count, user_yelping_since, "
                     f"user_useful, user_funny, user_cool, user_average_stars, "
                     f"user_compliment_cute, user_compliment_cool, user_compliment_funny "
                     f"from users")
        df = session.execute(query)
        df = toDataFrame(df)

    # 将 user_yelping_since 转换为天数
    df['user_yelping_since'] = pd.to_datetime(df['user_yelping_since'])
    df['user_yelping_days'] = (datetime.now() - df['user_yelping_since']).dt.days

    # 删除原始的 user_yelping_since 列
    df = df.drop(columns=['user_yelping_since'])

    # 标准化数据
    scaler = StandardScaler()
    features = ['user_review_count', 'user_yelping_days', 'user_useful', 'user_funny', 'user_cool',
                'user_average_stars', 'user_compliment_cute', 'user_compliment_cool', 'user_compliment_funny']
    df[features] = scaler.fit_transform(df[features])

    # k_list = [50, 100, 200]
    k_list = [20, 30, 40]
    # 选择 K 值
    wcss = []
    for i in k_list:
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(df[features])
        wcss.append(kmeans.inertia_)
        dump(kmeans, f'kmeans_model{i}.joblib')
        print(i)



    # 绘制肘部法则图
    import matplotlib.pyplot as plt

    plt.figure(figsize=(20, 16))
    plt.plot(k_list, wcss)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')  # Within cluster sum of squares
    plt.show()

    # # 假设从图中我们决定 K 值为 5
    # k_value = 5
    #
    # # 应用 K-Means 聚类
    # kmeans = KMeans(n_clusters=k_value, init='k-means++', max_iter=300, n_init=10, random_state=0)
    # df['cluster'] = kmeans.fit_predict(df[features])
    #
    # # 现在 df['cluster'] 包含了每个用户的聚类标签
    # print(df[['user_id', 'cluster']])


def calculate_accuracy(kmeans_model, df, X, sample_size=10):
    predictions = kmeans_model.predict(X)
    df['cluster'] = predictions

    # 创建一个簇ID到用户ID列表的映射
    cluster_to_users = df.groupby('cluster')['user_id'].apply(list).to_dict()

    # 计算准确率
    user_accuracies = []
    for cluster_id, users in cluster_to_users.items():
        if len(users) <= 1:
            continue  # 如果簇中只有一个用户，则跳过

        # 随机选择用户，数量为sample_size或簇中用户数，取较小值
        sampled_users = random.sample(users, min(sample_size, len(users)))

        for user_id in sampled_users:
            user_friends = df.loc[df['user_id'] == user_id, 'user_friends'].values[0]
            cluster_size = len(users)
            friend_count = sum(friend in user_friends for friend in users)
            accuracy = friend_count / cluster_size
            user_accuracies.append(accuracy)

    # 返回平均准确率
    return sum(user_accuracies) / len(user_accuracies) if user_accuracies else 0

def accuraciesTestRun():
    db_init(config.DATABASE_URL)
    with get_session() as session:
        query = text(f"select user_id, user_friends, user_review_count, user_yelping_since, "
                     f"user_useful, user_funny, user_cool, user_average_stars, "
                     f"user_compliment_cute, user_compliment_cool, user_compliment_funny "
                     f"from users")
        df = session.execute(query)
        df = toDataFrame(df)
    accuracy_results = {}
    df['user_yelping_since'] = pd.to_datetime(df['user_yelping_since'])
    df['user_yelping_days'] = (datetime.now() - df['user_yelping_since']).dt.days
    X = df.drop(columns=['user_id', 'user_friends', 'user_yelping_since']).values
    print(1)
    for k in [20, 30, 40, 50]:
        kmeans_model = joblib.load(f'kmeans_model{k}.joblib')
        print(2)
        accuracy = calculate_accuracy(kmeans_model, df, X)
        print(3)
        accuracy_results[k] = accuracy
        print(f'Model with k={k}: Accuracy = {accuracy}')

    # 找到准确率最高的模型
    best_k = max(accuracy_results, key=accuracy_results.get)
    print(f'Model with k={best_k} has the highest accuracy of {accuracy_results[best_k]}')
# db_init(config.DATABASE_URL)
# userClassification()

# def recommendRun(user_id, X, n_clusters=50):
#     kmeans = KMeans(n_clusters=n_clusters, random_state=0)
#     kmeans.fit(X)
#
#     # 预测簇标签
#     clusters = kmeans.predict(X)
#
#     # 创建一个字典，以簇标签为键，以属于该簇的用户ID列表为值
#     clustered_users = {}
#     for cluster_id in clusters:
#         if cluster_id not in clustered_users:
#             clustered_users[cluster_id] = []
#         clustered_users[cluster_id].append(user_id)

# 定义一个函数来随机推荐好友

def recommend_friends(user_id, clustered_users, n_recommendations=10):
    # 找到用户所在的簇
    for cluster_id, users in clustered_users.items():
        if user_id in users:
            # 从该簇中除了用户自己以外的用户列表中随机选择
            possible_friends = [uid for uid in users if uid != user_id]
            break
    else:
        return []  # 如果用户ID不在列表中，则返回空列表

    # 随机选取推荐的好友数量
    num_recommendations = min(n_recommendations, len(possible_friends))

    # 随机选择并返回推荐的好友
    return np.random.choice(possible_friends, num_recommendations, replace=False).tolist()

    # 假设有一个用户的ID是user_id_to_recommend
    user_id_to_recommend = user_ids[0]  # 举例来说，我们取第一个用户的ID

    # 获取推荐的好友列表
    recommended_friend_ids = recommend_friends(user_id_to_recommend, clustered_users, n_recommendations=10)

    # 打印推荐的好友用户ID
    print("Recommended Friends for User ID", user_id_to_recommend, ":", recommended_friend_ids)

db_init(config.DATABASE_URL)
with get_session() as session:
    query = text(f"select user_id, user_friends, user_review_count, user_yelping_since, "
                 f"user_useful, user_funny, user_cool, user_average_stars, "
                 f"user_compliment_cute, user_compliment_cool, user_compliment_funny "
                 f"from users")
    df = session.execute(query)
    df = toDataFrame(df)
accuracy_results = {}
df['user_yelping_since'] = pd.to_datetime(df['user_yelping_since'])
df['user_yelping_days'] = (datetime.now() - df['user_yelping_since']).dt.days
X = df.drop(columns=['user_id', 'user_friends', 'user_yelping_since']).values
loaded_kmeans = load('kmeans_model50.joblib')
clusters = loaded_kmeans.predict(X)

user_ids = df['user_id'].head(50).tolist()
# 创建一个字典，以簇标签为键，以属于该簇的用户ID列表为值
clustered_users = {}
for user_id, cluster_id in zip(user_ids, clusters):
    if cluster_id not in clustered_users:
        clustered_users[cluster_id] = []
    clustered_users[cluster_id].append(user_id)
# 假设有一个用户的ID是user_id_to_recommend
user_id_to_recommend = user_ids[0]  # 举例来说，我们取第一个用户的ID

# 获取推荐的好友列表
recommended_friend_ids = recommend_friends(user_id_to_recommend, clustered_users, n_recommendations=10)

# 打印推荐的好友用户ID
print("Recommended Friends for User ID", user_id_to_recommend, ":", recommended_friend_ids)


