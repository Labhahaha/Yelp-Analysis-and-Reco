from flask import Blueprint

#创建蓝图
business = Blueprint('business', __name__)

#先创建蓝图，再导入功能类，避免循环导入
from . import Business


