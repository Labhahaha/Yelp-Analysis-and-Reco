from flask import request, Blueprint

user_id =  None
business_id = None

login_blue = Blueprint('login', __name__)

@login_blue.route('/login')
def login():
    login_type = request.args.get('type')
    if login_type == "user":
        pass
        # user_id = request.args.get('id')
        # user_id = ''
    elif login_type == "business":
        pass
        # business_id = request.args.get('id')
    return 'login success'
