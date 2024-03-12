# coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
from ..Recommendation.Recommend import get_business_by_city

# ������ͼ
search_blue = Blueprint('search', __name__, )

df=None

# ��ȡ�̻�����
@search_blue.route('/')
def search():
    # ��ȡ��ѯ����
    query = request.args.get('query')
    if query is None:
        return jsonify({"error": "Missing query parameter"}), 400

    df = get_business_by_city('New Orleans')

    df = df[df['name'].str.contains(query, case=False)]

    # ��ȡ�������(��ѡ)
    sortBy = request.args.get('sortBy')

    if sortBy == 'stars':
        # �����Ǽ��Ӹߵ�������
        df = df.sort_values(by='stars', ascending=False)

    if sortBy == 'review_count':
        # �������������Ӹߵ�������
        df = df.sort_values(by='review_count', ascending=False)
        print(df)

    if sortBy == 'distance':
        # ���վ���ӽ���Զ����
        df = df.sort_values(by='distance')


    # ������������֡ת��Ϊ JSON ��ʽ
    json_res = df.to_json(orient='records')

    return json_res, 200

