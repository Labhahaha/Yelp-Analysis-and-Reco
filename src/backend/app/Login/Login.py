from flask import request, Blueprint,jsonify
from ..Recommendation import Recommend
login_blue = Blueprint('login', __name__)

@login_blue.route('/')
def login():
    map_list = {
        'Buton':'mgdpBWceTxl_0ffDOoauSQ',
        'Shari':'gmwE4HCfTysGMGT-jCuaPg'
    }
    login_type = request.args.get('type')
    name = request.args.get('name')
    if login_type == "user":
        Recommend.user_id = map_list[name]
        return jsonify({'status':'success'})
    elif login_type == "business":
        Recommend.user_id = map_list[name]
        return jsonify({'status':'success'})

