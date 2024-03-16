from flask import request, Blueprint,jsonify
from ..Recommendation import Recommend
login_blue = Blueprint('login', __name__)

@login_blue.route('/')
def login():
    # 登录用户名和ID映射
    map_list = {
        'Buton':'mgdpBWceTxl_0ffDOoauSQ',
        'Shari':'gmwE4HCfTysGMGT-jCuaPg'
    }
    # 登录类型参数
    login_type = request.args.get('type')
    name = request.args.get('name')
    # 用户商户登录，更新全局ID
    if login_type == "user":
        Recommend.user_id = map_list[name]
        return jsonify({'status':'success'})
    elif login_type == "business":
        return jsonify({'status':'success'})

