import joblib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE
from sqlalchemy import text
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime
from joblib import dump
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.decomposition import PCA
from contextlib import contextmanager
engine = None
Session = None


@contextmanager
def get_session():
    if Session is None:
        raise Exception("Database not initialized. Call db_init() first.")
    session = Session()
    try:
        yield session
    finally:
        session.close()


def toDataFrame(res):
    data = [row._asdict() for row in res]
    df = pd.DataFrame(data)
    return df


def db_init(db_url):
    global engine, Session
    if engine is None:
        # 创建数据库引擎
        engine = create_engine(db_url)
        # 创建会话工厂
        Session = sessionmaker(bind=engine)


# 使用kmeans对用户进行聚类
def userClassification():
    db_init('mysql+pymysql://root:123456@localhost:3306/yelp')
    with get_session() as session:
        query = text(f"SELECT * FROM users")
        df = session.execute(query)
        df = toDataFrame(df)
    # 处理特征
    df['user_friends_count'] = df['user_friends'].str.count(', ')
    df = df.drop(columns=['user_friends'])
    df['user_average_stars'] = df['user_average_stars'].astype(int)

    # 定义特征参数
    features = ['user_friends_count', 'user_average_stars', 'user_review_count', 'user_useful', 'user_funny',
                'user_cool', 'user_fans', 'user_compliment_hot', 'user_compliment_more', 'user_compliment_profile',
                'user_compliment_cute', 'user_compliment_list', 'user_compliment_note', 'user_compliment_plain',
                'user_compliment_cool', 'user_compliment_funny', 'user_compliment_writer', 'user_compliment_photos']

    # 归一化数据
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])
    # 主成分分析法降维
    pca = PCA(n_components=10, random_state=42)  # 指定降维后的维度
    pca.fit(df[features])
    pca_feature = pca.transform(df[features])
    dump(pca, f'pca10.joblib')
    # 对不同的k值训练模型
    for k in [10, 15, 25, 30, 35, 40, 45, 50, 100]:
        print(f"开始训练模型：k={k}")
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=42)
        kmeans.fit(pca_feature)
        dump(kmeans, f'D:/2024shixun/ProjectCode/Yelp-Analysis-and-Reco/src/backend/config/model/kmeans_model{k}.joblib')

        # 随机取样10000个
        sampled_indices = np.random.choice(pca_feature.shape[0], 10000, replace=False)
        sampled_data = pca_feature[sampled_indices]

        # 使用TSNE进行降维
        tsne = TSNE(n_components=2)
        df_tsne = tsne.fit_transform(sampled_data)

        # 绘制聚类结果
        plt.scatter(df_tsne[:, 0], df_tsne[:, 1], c=kmeans.labels_[sampled_indices], cmap='viridis', alpha=0.5, s=5)
        plt.title('KMeans10000个样本点聚类图')
        plt.legend()
        plt.show()


userClassification()


# 计算准确率
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


# 调用计算准确率的函数
def accuraciesTestRun():
    # db_init(config.DATABASE_URL)
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
    for k in [10, 15, 20, 30, 40, 50, 100]:
        kmeans_model = joblib.load(f'kmeans_model{k}.joblib')
        accuracy = calculate_accuracy(kmeans_model, df, X)
        accuracy_results[k] = accuracy
        print(f'k={k}：准确率为{accuracy}')

    # 找到准确率最高的模型
    best_k = max(accuracy_results, key=accuracy_results.get)
    print(f'k={best_k}准确率最高，准确率为{accuracy_results[best_k]}')






