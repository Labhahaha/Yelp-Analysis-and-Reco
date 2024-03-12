from sqlalchemy import text

from ..DataAnalyse.SQLSession import get_session, toDataFrame
def get_business_by_city(city):
    with get_session() as session:
        query = text(f"select * from business where city = '{city}'")
        res = session.execute(query)
        res = toDataFrame(res)
        return res