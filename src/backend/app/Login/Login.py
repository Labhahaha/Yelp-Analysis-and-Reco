from flask import request, Blueprint, jsonify

from ..Recommendation import Recommend

login_blue = Blueprint('login', __name__)


@login_blue.route('/')
def login():
    # 登录用户名和ID映射
    user_map_list = {
        'Buton': 'mgdpBWceTxl_0ffDOoauSQ',
        'Shari': 'gmwE4HCfTysGMGT-jCuaPg',

    }
    business_map_list = {
        'asdf': 'Pw77mNz6cso9quMp2NwaiA'
    }
    # 登录类型参数
    login_type = request.args.get('type')
    name = request.args.get('name')
    # 用户商户登录，更新全局ID
    if login_type == "user":
        if name in user_map_list:
            Recommend.user_id = user_map_list[name]
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'not exit user'})
    elif login_type == "business":
        if name in business_map_list:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'not exit business'})
