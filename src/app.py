# coding:utf-8
# 引入 Flask 类
from flask import Flask
from TextRandJob import TextRandJob

# 实例化一个 Flask 对象
app = Flask(__name__)


@app.route('/')
def hello_world():
    res = TextRandJob().start()
    collect = res.toJSON().collect()
    return collect.toJSON()


# 如果这个脚本是直接运行的，则启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
