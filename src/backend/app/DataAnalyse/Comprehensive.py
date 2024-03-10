from flask import Blueprint
from sqlalchemy import text
from .SQLSession import get_session, toJSON, ToDataFrame
# 创建蓝图
comprehensive_blue = Blueprint('comprehensive', __name__,)


# 每个城市最好（评分次数、评分、打卡数）的五家商家
@comprehensive_blue.route('/comprehensive_analysis')
def comprehensive_analysis():
    with get_session() as session:
        query = text("select * from comprehensive_analysis")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res

