from flask import Blueprint
from sqlalchemy import text

from .SQLSession import get_session, toJSON

# ������ͼ
users_blue = Blueprint('users', __name__, )


# ͳ��ÿ�������û�����
@users_blue.route('/user_count_by_registration_year')
def user_count_by_registration_year():
    with get_session() as session:
        query = text("select * from user_count_by_registration_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ�����۴���
@users_blue.route('/user_with_most_review')
def user_with_most_review():
    with get_session() as session:
        query = text("select * from user_with_most_review")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ��������ߵ��û�
@users_blue.route('/user_with_most_fans')
def user_with_most_fans():
    with get_session() as session:
        query = text("select * from user_with_most_fans")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ��ÿ�������û�����ͨ�û�����
@users_blue.route('/elite_user_ratio')
def elite_user_ratio():
    with get_session() as session:
        query = text("select * from elite_user_ratio")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ��ʾÿ�����û�������Ĭ�û�����δд���ۣ��ı���
@users_blue.route('/silent_user_ratio')
def silent_user_ratio():
    with get_session() as session:
        query = text("select * from silent_user_ratio")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ�Ƴ�ÿ���������
@users_blue.route('/review_count_bu_year')
def review_count_bu_year():
    with get_session() as session:
        query = text("select * from review_count_bu_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ�Ƴ�ÿ��ľ�Ӣ�û�
@users_blue.route('/elite_user_count_by_year')
def elite_user_count_by_year():
    with get_session() as session:
        query = text("select * from elite_user_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ�Ƴ�ÿ���tip��
@users_blue.route('/tip_count_by_year')
def tip_count_by_year():
    with get_session() as session:
        query = text("select * from tip_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# ͳ�Ƴ�ÿ��Ĵ���
@users_blue.route('/checkin_count_by_year')
def checkin_count_by_year():
    with get_session() as session:
        query = text("select * from checkin_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res
