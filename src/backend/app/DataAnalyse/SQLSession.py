from contextlib import contextmanager

import pandas as pd
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
Session = None


def db_init(db_url):
    global engine, Session
    if engine is None:
        # 创建数据库引擎
        engine = create_engine(db_url)
        # 创建会话工厂
        Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    if Session is None:
        raise Exception("Database not initialized. Call db_init() first.")
    session = Session()
    try:
        yield session
    finally:
        session.close()


def toJSON(res):
    res = [row._asdict() for row in res]
    json_res = jsonify(res)
    return json_res


def ToDataFrame(res):
    data = [dict(row) for row in res]
    df = pd.DataFrame(data)
    return df
