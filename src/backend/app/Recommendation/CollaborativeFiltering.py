import pandas as pd
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from surprise import Dataset, dump
from surprise import Reader
from surprise import SVD
from surprise.model_selection import train_test_split
model_path = 'config/model/filter_model.pkl'
model = dump.load(model_path)[1]
reader = Reader(rating_scale=(1, 5))

def model_train():
    #加载训练数据
    with get_session() as session:
        query = text("select rev_user_id, rev_business_id, rev_stars from review")
        res = session.execute(query)
        review_df = toDataFrame(res)
    data = Dataset.load_from_df(review_df[['rev_user_id', 'rev_business_id', 'rev_stars']], reader)
    print('数据加载完成')
    #训练测试分割
    trainset, testset = train_test_split(data, test_size=0.05)
    #定义模型
    model = SVD()
    # 训练模型
    model.fit(trainset)
    print('模型训练完成')
    # 保存模型
    dump.dump(model_path, algo=model)

def model_test():
    with get_session() as session:
        query = text("select rev_user_id, rev_business_id, rev_stars from review")
        res = session.execute(query)
        review_df = toDataFrame(res)
    data = Dataset.load_from_df(review_df[['rev_user_id', 'rev_business_id', 'rev_stars']], reader)
    print('数据加载完成')
    #训练测试分割
    trainset, testset = train_test_split(data, test_size=0.05)
    # 加载模型
    model = dump.load(model_path)[1]
    print('模型加载完成')
    predictions = model.test(testset)
    print('模型预测完成')
    print(predictions)

def CollaborativeFiltering(user_id, business_ids):
    business_ids['user_id'] = user_id
    business_ids['true_rating'] = 1
    data = business_ids
    data = Dataset.load_from_df(data[['user_id', 'business_id','true_rating']],reader)
    data = data.build_full_trainset().build_testset()
    predictions = model.test(data)
    df_predictions = toDataFrame(predictions)
    return df_predictions

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




