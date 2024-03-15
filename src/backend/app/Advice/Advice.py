from flask import Blueprint, jsonify
import json
import requests
from .Sentiment import analyze_reviews_for_business

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=4qY7CsNN4WsWWfMAj45dCZV4&client_secret=8yziqhq6wQUo5VcGKo1bRxl0jXhvxiMe"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json().get("access_token"))

    return response.json().get("access_token")


def get_api_response(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"我是一名餐厅商家，以下是我最近得到的差评，分析并从中提取关键信息,给我列出五条简洁的经营建议，只需返回中文建议内容：{text}"
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

advice_blue = Blueprint('advice', __name__)


def get_top_five_businesses(business_df):
    # 根据综合评分降序排序，并取前五个商家
    top_five_businesses_df = business_df.nlargest(5, 'weighted_score')
    return top_five_businesses_df

def get_common_attributes(business_df):

    # 获取前五商家的DataFrame
    top_five_businesses_df = get_top_five_businesses(business_df)

    # 初始化共有Attributes字典
    common_attributes = {}

    # 记录每个属性出现的次数
    attribute_count = {}

    # 遍历前五商家的Attributes，逐个进行统计
    for index, row in top_five_businesses_df.iterrows():
        attributes_json = row['attributes']
        try:
            attributes = json.loads(attributes_json.replace('u\'', '"').replace('\'', '"'))
        except json.JSONDecodeError:
            continue  # 如果Attributes解析失败，跳过此商家

        if not isinstance(attributes, dict):
            continue  # 如果Attributes不是字典类型，跳过此商家

        # 统计当前商家的Attributes
        for key, value in attributes.items():
            attribute_count[(key, value)] = attribute_count.get((key, value), 0) + 1

    # 遍历属性计数，提取出在至少两家商家中共有的属性
    for (key, value), count in attribute_count.items():
        if count >= 2:
            common_attributes[key] = value

    return common_attributes

def analyze_negative_reviews(review_df):
    # 筛选出 rev_stars 为 1 或 2 的评论
    negative_reviews = review_df[(review_df['rev_stars'] == 1) | (review_df['rev_stars'] == 2)]

    # 提取评论文本
    negative_reviews_text = negative_reviews['rev_text'].tolist()

    suggestions = get_api_response("\n".join(negative_reviews_text))
    return suggestions

@advice_blue.route('/get_advice')
def get_advice():
    global business_df, review_df

    common_attributes = get_common_attributes(business_df)

    top_five_businesses = get_top_five_businesses(business_df)

    negative_reviews_advice = analyze_negative_reviews(review_df)

    positive_reviews_count,negative_reviews_count,normal_reviews_count = analyze_reviews_for_business(review_df)
    res = {
        'common_attributes': common_attributes,
        'top_five_businesses': top_five_businesses.to_dict(orient='records'),
        'negative_reviews_advice': negative_reviews_advice,
        'reviews_count': [int(positive_reviews_count), int(negative_reviews_count), int(normal_reviews_count)],
    }

    json_res = jsonify(res)
    return json_res