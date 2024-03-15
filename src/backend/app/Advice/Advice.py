from flask import Blueprint, jsonify
import os
from openai import OpenAI


os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"


client = OpenAI(
    api_key="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"
)

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

    # 遍历前五商家的Attributes，逐个进行比较
    for index, row in top_five_businesses_df.iterrows():
        attributes = row['attributes']
        if not isinstance(attributes, dict):
            continue  # 如果Attributes不是字典类型，跳过此商家
        if not common_attributes:  # 如果共有Attributes为空，直接复制当前商家的Attributes
            common_attributes = attributes
        else:
            # 比较当前商家的Attributes与共有Attributes，保留共有的Attributes
            for key, value in attributes.items():
                if key in common_attributes and common_attributes[key] != value:
                    del common_attributes[key]

    return common_attributes

def analyze_negative_reviews(review_df):
    # 筛选出 rev_stars 为 1 或 2 的评论
    negative_reviews = review_df[(review_df['rev_stars'] == 1) | (review_df['rev_stars'] == 2)]

    # 提取评论文本
    negative_reviews_text = negative_reviews['rev_text'].tolist()

    # 调用 OpenAI API
    input_text = "\n".join(negative_reviews_text)

    # 调用 OpenAI GPT-3.5 API 进行分析
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"我是一名商家，以下是我最近得到的差评，请你分析并从中提取信息,给我列出五条经营建议，只需要返回建议内容：【{input_text}】。"
            }
        ],
        model="gpt-3.5-turbo",
    )
    # 提取 API 响应中的文本部分作为改进建议
    suggestions = chat_completion.choices[0].message.content

    return suggestions
@advice_blue.route('/get_advice')
def get_advice():
    global business_df, review_df

    common_attributes = get_common_attributes(business_df)

    top_five_businesses = get_top_five_businesses(business_df)

    negative_reviews_advice = analyze_negative_reviews(review_df)

    res = {
        'common_attributes': common_attributes,
        'top_five_businesses': top_five_businesses.to_dict(orient='records'),
        'negative_reviews_advice': negative_reviews_advice.to_dict(orient='records')
    }

    json_res = jsonify(res)
    return json_res