# coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
from ..utils import get_business_by_city, cal_distance
from .Filter import filter

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

    # �����л�ȡ�̼�����
    df = get_business_by_city('Abington')

    # �����û���ÿһ���̼ҵľ��룬df������distance��
    df['distance'] = df.apply(lambda row: cal_distance([-75.111,40.1282], [row['longitude'], row['latitude']]), axis=1)

    # ����ģ����ѯ
    df = df[df['name'].str.contains(query, case=False)]

    # ��ȡ�������(��ѡ)
    sortBy = request.args.get('sortBy')

    # ��������(��ѡ)
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

    # ��ȡɸѡ����(��ѡ)
    filter_type = request.args.get('filter')
    filter_condition = request.args.get("filter_condition")

    # ����ɸѡ(��ѡ)
    df=filter(df,filter_type,filter_condition)


    # ������/ɸѡ�������ת��Ϊ JSON ��ʽ
    json_res = df.to_json(orient='records')

    return json_res, 200

