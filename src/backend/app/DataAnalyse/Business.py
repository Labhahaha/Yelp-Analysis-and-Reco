from flask import Blueprint
from sqlalchemy import text
from .SQLSession import get_session,toJSON,ToDataFrame
#创建蓝图
business_blue= Blueprint('business', __name__,)

#找出美国最常见商户（前n）
@business_blue.route('/search_most_business')
def search_most_business():
    with get_session() as session:
        query = text("select * from most_common_business")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res

#找出美国商户最多的城市
def search_most_city(num=10):
    pass

#找出美国商户最多的州
def search_most_state(self,num=5):
    pass

#找出美国最常见商户并显示平均评分
def search_most_star(self,num=20):
    pass




