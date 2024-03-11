#coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
from sqlalchemy import text

from ..DataAnalyse.SQLSession import (get_session, toJSON)

# 创建蓝图
business_details_blue = Blueprint('business_details', __name__, )


# 获取商户详情
@business_details_blue.route('/business_details')
def business_details():
    business_id = request.args.get('id')
    if not business_id:
        return jsonify({"error": "Missing business_id parameter"}), 400
    with get_session() as session:
        query_business = text("select * from business where business_id = :business_id")
        res_business = session.execute(query_business,{"business_id": business_id})
        query_review = text("select * from review where rev_business_id = :rev_business_id")
        res_review = session.execute(query_review,{"rev_business_id": business_id})
        json_res = {
            "business": json.loads(toJSON_str(res_business)),
            "reviews": json.loads(toJSON_str(res_review))
        }
        return jsonify(json_res), 200
def toJSON_str(res):
    res = [row._asdict() for row in res]
    json_str = json.dumps(res)
    return json_str