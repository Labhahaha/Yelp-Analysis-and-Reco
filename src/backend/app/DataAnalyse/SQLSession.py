from contextlib import contextmanager

import pandas as pd
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 数据库引擎
engine = None
# 会话工程
Session = None


# 数据库初始化
def db_init(db_url):
    global engine, Session
    if engine is None:
        # 创建数据库引擎
        engine = create_engine(db_url)
        # 创建会话工厂
        Session = sessionmaker(bind=engine)


# 创建数据库会话上下文管理器，实现数据库查询会话的自动创建和关闭
@contextmanager
def get_session():
    if Session is None:
        raise Exception("Database not initialized. Call db_init() first.")
    session = Session()
    try:
        # 创建会话
        yield session
    finally:
        # 关闭会话
        session.close()


# 数据库结果转json工具函数
def toJSON(res):
    res = [row._asdict() for row in res]
    json_res = jsonify(res)
    return json_res


# 数据库结果转dataframe工具函数
def toDataFrame(res):
    data = [row._asdict() for row in res]
    df = pd.DataFrame(data)
    return df
