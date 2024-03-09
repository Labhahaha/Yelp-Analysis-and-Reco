from flask import Blueprint
from .Business import Business


business_blue = Blueprint('business', __name__, url_prefix='/business')
review_blue = Blueprint('review', __name__, url_prefix='/review')
user_blue = Blueprint('user', __name__, url_prefix='/user')

business = Business()

@business_blue.route('/search_most_business')
def search_most_business(num=20):
    res = business.search_most_business()
    res = res.toJSON().collect()
    return res





