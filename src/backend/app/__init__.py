from flask import Flask
from flask_cors import CORS

def create_app():
    #实例化app
    app = Flask(__name__)

    #导入蓝图
    from .DataAnalyse import business as business_blue
    app.register_blueprint(business_blue, url_prefix='/business')

    CORS(app, supports_credentials=True)

    return app



