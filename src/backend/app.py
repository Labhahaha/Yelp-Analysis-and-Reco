from flask import Flask
from DataAnalyse import business_blue
from flask_cors import CORS

# 实例化一个 Flask 对象
app = Flask(__name__)

app.register_blueprint(business_blue,)
CORS(app, supports_credentials=True)

app.run(debug=True)
