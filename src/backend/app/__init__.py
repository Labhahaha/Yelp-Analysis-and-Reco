from flask import Flask
from flask_cors import CORS

from .DataAnalyse import business_blue, users_blue, checkin_blue, comprehensive_blue, stars_blue, db_init, \
    review_blue, filter_words
from .Recommendation import recommend_blue
from .Advice import boards_blue, advice_blue
from .Friends import friends_blue
from .Login import login_blue
from .Search import search_blue


def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    db_init(config.DATABASE_URL)
    app.register_blueprint(business_blue, url_prefix='/business')
    app.register_blueprint(users_blue, url_prefix='/users')
    app.register_blueprint(checkin_blue, url_prefix='/checkin')
    app.register_blueprint(stars_blue, url_prefix='/stars')
    app.register_blueprint(comprehensive_blue, url_prefix='/comprehensive')
    app.register_blueprint(review_blue, url_prefix='/review')
    app.register_blueprint(recommend_blue, url_prefix='/recommend')
    app.register_blueprint(search_blue, url_prefix='/search')
    app.register_blueprint(friends_blue, url_prefix='/friends')
    app.register_blueprint(login_blue, url_prefix='/login')
    app.register_blueprint(boards_blue, url_prefix='/boards')
    app.register_blueprint(advice_blue, url_prefix='/advice')

    return app
