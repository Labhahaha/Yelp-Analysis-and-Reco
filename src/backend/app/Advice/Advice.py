import json

from flask import Blueprint, jsonify

reviews_count = None
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


@advice_blue.route('/get_advice')
def get_advice():
    global business_df, review_df, negative_reviews_advice

    common_attributes = get_common_attributes(business_df)

    top_five_businesses = get_top_five_businesses(business_df)

    res = {
        'common_attributes': common_attributes,
        'top_five_businesses': top_five_businesses.to_dict(orient='records'),
        'negative_reviews_advice': negative_reviews_advice,
        'reviews_count': [int(reviews_count[0]), int(reviews_count[1]), int(reviews_count[2])],
    }

    json_res = jsonify(res)
    return json_res
