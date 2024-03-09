from flask import Blueprint
from .Business import Business

business = Business()

business_blue = Blueprint('business', __name__, url_prefix='/business')
review_blue = Blueprint('review', __name__, url_prefix='/review')
user_blue = Blueprint('user', __name__, url_prefix='/user')



# @business_blue.route('/search_most_business')
# def search_most_business(num=20):
#     res = business.search_most_business(num)
#     res = res.toJSON().collect()
#     return res
# @business_blue.route('/search_most_city')
# def search_most_city(self,num=10):
#     res = business.search_most_city(num)
#     res = res.toJSON().collect()
#     return res
# @business_blue.route('/search_most_state')
# def search_most_state(self,num=5):
#     res = business.search_most_state(num)
#     res = res.toJSON().collect()
#     return res
# @business_blue.route('/search_most_star')
# def search_most_state(self,num=5):
#     res = business.search_most_star(num)
#     res = res.toJSON().collect()
#     return res





