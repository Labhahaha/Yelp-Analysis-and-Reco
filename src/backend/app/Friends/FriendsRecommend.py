from flask import Blueprint, jsonify, json
from flask import request
from sqlalchemy import text
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from src.backend.app.DataAnalyse.SQLSession import (get_session, toJSON, toDataFrame, db_init)
from src.backend.config import config
import pandas as pd
from sklearn.impute import SimpleImputer
from datetime import datetime
import pickle

friends_blue = Blueprint('Friends', __name__)
# 111


@friends_blue.route("/")
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





