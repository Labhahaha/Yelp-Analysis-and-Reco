from sqlalchemy import text

from .Sentiment import sentiment_predict
from .Boards import boards_blue
from .Advice import advice_blue
from ..DataAnalyse.SQLSession import get_session, toDataFrame


