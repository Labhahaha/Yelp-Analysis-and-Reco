from flask import Flask
from flask_cors import CORS
from .DataAnalyse import business_blue,users_blue,db_init

def create_app(config):
    #ÊµÀý»¯app
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    db_init(config.DATABASE_URL)

    app.register_blueprint(business_blue, url_prefix='/business')

    app.register_blueprint(users_blue, url_prefix='/users')

    return app



