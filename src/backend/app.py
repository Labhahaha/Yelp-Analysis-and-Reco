from flask import Flask
from flask_cors import CORS
from config import config
from DataAnalyse import business_blue,db_init

# 实例化一个 Flask 对象
app = Flask(__name__)
CORS(app, supports_credentials=True)

#初始化数据库连接
db_init(config.DATABASE_URL)
#注册路由和视图函数
app.register_blueprint(business_blue)

#启动应用
app.run(host="0.0.0.0",port=5000,debug=True)