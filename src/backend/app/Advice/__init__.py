from sqlalchemy import text

from .Sentiment import sentiment_predict
from .Boards import boards_blue
from .Advice import advice_blue
from ..DataAnalyse.SQLSession import get_session, toDataFrame


def get_head_business(business_id):
    with get_session() as session:
        query = text("select * from business_with_most_5stars")
        res = session.execute(query)
        df_res = toDataFrame(res)
