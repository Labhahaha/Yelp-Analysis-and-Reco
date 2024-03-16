import pandas as pd
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session
from surprise import Dataset, dump
from surprise import Reader
from surprise import SVD,SVDpp
from surprise.model_selection import train_test_split

'''
根据用户历史消费和点评记录，实现基于矩阵分解和隐式反馈信息的协同过滤推荐算法
'''

# 模型地址和加载
model_path = 'config/model/filter_model.pkl'
model_pp_path = 'config/model/filter_model+.pkl'
model = dump.load(model_pp_path)[1]
# 数据归一化
reader = Reader(rating_scale=(1, 5))


def model_train():
    # 加载训练数据，包含用户和商户的点评数据
    with get_session() as session:
        query = text("select rev_user_id, rev_business_id, rev_stars from review")
        res = session.execute(query)
        review_df = toDataFrame(res)
    data = Dataset.load_from_df(review_df[['rev_user_id', 'rev_business_id', 'rev_stars']], reader)
    print('数据加载完成')
    # 训练集和测试集分割
    trainset, testset = train_test_split(data, test_size=0.05)
    # 定义矩阵分解模型
    model = SVDpp()
    # 训练模型
    model.fit(trainset)
    print('模型训练完成')
    # 保存模型
    dump.dump(model_pp_path, algo=model)


def model_test():
    with get_session() as session:
        query = text("select rev_user_id, rev_business_id, rev_stars from review")
        res = session.execute(query)
        review_df = toDataFrame(res)
    data = Dataset.load_from_df(review_df[['rev_user_id', 'rev_business_id', 'rev_stars']], reader)
    print('数据加载完成')
    # 训练测试分割
    trainset, testset = train_test_split(data, test_size=0.05)
    # 加载模型
    model = dump.load(model_path)[1]
    print('模型加载完成')
    predictions = model.test(testset)
    print('模型预测完成')
    print(predictions)


def CollaborativeFiltering(user_id, business_ids):
    # 获取用户id
    business_ids['user_id'] = user_id
    business_ids['true_rating'] = 1
    # 加载带推理商户数据
    data = business_ids
    data = Dataset.load_from_df(data[['user_id', 'business_id', 'true_rating']], reader)
    data = data.build_full_trainset().build_testset()
    # 使用协同过滤模型预测用户评价
    predictions = model.test(data)
    # 返回预测的用户对商户的评价分数列表
    df_predictions = toDataFrame(predictions)
    return df_predictions


# 返回用户id和商户id和预测打分的列表
def toDataFrame(predictions):
    prediction_list = []
    for prediction in predictions:
        uid = prediction.uid
        iid = prediction.iid
        predicted_rating = prediction.est
        prediction_dict = {
            'user_id': uid,
            'business_id': iid,
            'rating': predicted_rating
        }
        prediction_list.append(prediction_dict)
    df_predictions = pd.DataFrame(prediction_list)
    return df_predictions
