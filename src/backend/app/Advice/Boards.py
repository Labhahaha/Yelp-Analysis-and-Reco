from threading import Thread

import json
import requests
from flask import Blueprint, jsonify
from sqlalchemy import text

from .Sentiment import analyze_reviews_for_business
from ..Advice import Advice
from ..DataAnalyse.SQLSession import get_session, toDataFrame
from ..Recommendation.Recommend import get_business_by_city

# 替换为你的文心一言API_TOKEN
API_TOKEN = ""

boards_blue = Blueprint('boards', __name__)

business_df = None
review_df = None


def extract_category(categories):
    # 以逗号为分隔符将字符串拆分成列表
    category_list = categories.split(',')

    # 遍历列表，找到第一个包含 'Restaurants' 的类别
    for category in category_list:
        if 'Restaurants' in category:
            return category.strip()  # 去除首尾空格并返回找到的类别

    # 如果列表中没有包含 'Restaurants' 的类别，则返回 None
    return None


def get_business_category(business_id):
    with get_session() as session:
        query = text("SELECT categories FROM business WHERE business_id = :business_id")
        res = session.execute(query, {"business_id": business_id})
        categories = res.fetchone()[0]

        # 提取类别信息
        category = extract_category(categories)
        return category


def get_similar_high_rated_businesses(business_id, threshold=4.5):
    category = get_business_category(business_id)
    with get_session() as session:
        query = text("""
            SELECT business_id, name, stars, review_count
            FROM business
            WHERE categories LIKE :category
            AND stars > :threshold
            AND is_open = 1
            ORDER BY stars DESC, review_count DESC
        """)
        res = session.execute(query, {"category": f'%{category}%', "threshold": threshold})
        res = toDataFrame(res)
        return res


# 获取当前商家在当前类别中的排名
def get_business_rank_in_category(business_id, business_df):
    # 获取当前商家的类别
    category = get_business_category(business_id)

    # 构建查询语句，查找当前商家在当前类别中的排名
    category_businesses = business_df[business_df['categories'].str.contains(category)]
    category_businesses = category_businesses[category_businesses['is_open'] == 1]

    # 计算星级的归一化分数
    min_stars = category_businesses['stars'].min()
    max_stars = category_businesses['stars'].max()
    category_businesses['normalized_stars'] = (category_businesses['stars'] - min_stars) / (max_stars - min_stars)

    # 计算综合评分，星级占70%，评论数量占30%
    normalized_review_count = (category_businesses['review_count'] - category_businesses['review_count'].min()) / (
            category_businesses['review_count'].max() - category_businesses['review_count'].min())
    category_businesses['weighted_score'] = 0.7 * category_businesses[
        'normalized_stars'] + 0.3 * normalized_review_count
    category_businesses = category_businesses.sort_values(by='weighted_score', ascending=False)
    category_businesses['category_rank'] = range(1, len(category_businesses) + 1)

    # 添加得分列
    business_df['weighted_score'] = category_businesses['weighted_score']
    Advice.business_df = business_df

    # 找出当前商家的排名
    business_rank = category_businesses.loc[category_businesses['business_id'] == business_id, 'category_rank'].iloc[0]

    return business_rank


def analyze_star_count(business_id):
    with get_session() as session:
        query = text(
            "select rev_stars, COUNT(*) as count from review WHERE rev_business_id = :business_id GROUP BY rev_stars")
        res = session.execute(query, {"business_id": business_id})
        res = toDataFrame(res)
    return res


# 获取特定business_id下的所有评论文本
def get_review_by_business(business_id):
    with get_session() as session:
        query = text("select * from review WHERE rev_business_id = :business_id ORDER BY rev_timestamp DESC")
        res = session.execute(query, {"business_id": business_id})
        res = toDataFrame(res)
        return res


def get_api_response(text):
    access_token = API_TOKEN
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + access_token

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"我是一名餐厅商家，以下是我最近得到的差评，分析并从中提取关键信息,给我列出三条经营建议，让答案尽可能简短，只返回中文建议内容：{text}"
            }
        ],
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_text = json.loads(response.text).get("result")

    return response_text


def analyze_negative_reviews(review_df):
    # 筛选出 rev_stars 为 1 的评论
    negative_reviews = review_df[(review_df['rev_stars'] == 1)]

    # 提取评论文本
    negative_reviews_text = negative_reviews['rev_text'].tolist()

    suggestions = get_api_response("\n".join(negative_reviews_text))

    Advice.negative_reviews_advice = suggestions

    return suggestions


@boards_blue.route('/get_board')
def get_board():
    # global business_df, review_df

    business_id = 'Pw77mNz6cso9quMp2NwaiA'
    business_df = get_business_by_city(city='Abington')
    review_df = get_review_by_business(business_id)

    # 开启线程后台请求文心一言回复
    api_response_thread = Thread(target=analyze_negative_reviews, args=(review_df,))
    api_response_thread.start()

    Advice.review_df = review_df
    star_count = analyze_star_count(business_id)
    business_rank = get_business_rank_in_category(business_id, business_df)
    Advice.reviews_count = analyze_reviews_for_business(review_df)

    res = {
        'business_details': business_df[business_df['business_id'] == business_id].to_dict(orient='records')[0],
        'reviews': review_df.to_dict(orient='records'),
        'star_count': star_count.to_dict(orient='records'),
        'business_rank': int(business_rank),
        'positive_reviews_count': int(Advice.reviews_count[0])
    }

    json_res = jsonify(res)
    return json_res
