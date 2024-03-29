from flask import Blueprint, jsonify
from nltk import pos_tag
from sqlalchemy import text

from .SQLSession import get_session, toJSON, toDataFrame

# 创建蓝图
review_blue = Blueprint('review', __name__, )


def filter_words():
    with get_session() as session:
        query = text("select * from top20_words")
        res = session.execute(query)
        res_df = toDataFrame(res)
        res_df['tag'] = res_df['word'].apply(lambda row: pos_tag([row])[0][1])
        n_df = res_df[res_df['tag'] == 'NN']
        a_df = res_df[res_df['tag'] == 'JJ']
        n_df.to_csv('n.csv', index=False)
        a_df.to_csv('a.csv', index=False)


@review_blue.route('/top20_words')
def top20_words():
    with get_session() as session:
        query = text("select * from top20_words")
        res = session.execute(query)
        res_df = toDataFrame(res)
        res_df['tag'] = res_df['word'].apply(lambda row: pos_tag([row])[0][1])
        res_df = res_df[res_df['tag'] == 'NN'].head(200)
        json_res = res_df[['word', 'word_count']].to_json(orient='records')
        return json_res


@review_blue.route('/top10_positive_words')
def top10_positive_words():
    with get_session() as session:
        query = text("select * from top10_positive_words")
        res = session.execute(query)
        res_df = toDataFrame(res)
        res_df['tag'] = res_df['word'].apply(lambda row: pos_tag([row])[0][1])
        res_df_n = res_df[res_df['tag'] == 'NN'].head(10)
        res_df_a = res_df[res_df['tag'] == 'JJ'].head(10)
        dict_res_n = res_df_n[['word', 'word_count']].to_dict(orient='records')
        dict_res_a = res_df_a[['word', 'word_count']].to_dict(orient='records')
        res = {
            'n': dict_res_n,
            'a': dict_res_a,
        }
        res = jsonify(res)
        return res


@review_blue.route('/top10_negative_words')
def top10_negative_words():
    with get_session() as session:
        query = text("select * from top10_negative_words")
        res = session.execute(query)
        res_df = toDataFrame(res)
        res_df['tag'] = res_df['word'].apply(lambda row: pos_tag([row])[0][1])
        res_df_n = res_df[res_df['tag'] == 'NN'].head(10)
        res_df_a = res_df[res_df['tag'] == 'JJ'].head(10)
        dict_res_n = res_df_n[['word', 'word_count']].to_dict(orient='records')
        dict_res_a = res_df_a[['word', 'word_count']].to_dict(orient='records')
        res = {
            'n': dict_res_n,
            'a': dict_res_a,
        }
        res = jsonify(res)
        return res


@review_blue.route('/different_review')
def different_review():
    with get_session() as session:
        query1 = text("select * from helpful_review")
        res1 = session.execute(query1)
        res1_df = toDataFrame(res1)
        query2 = text("select * from funny_review")
        res2 = session.execute(query2)
        res2_df = toDataFrame(res2)
        query3 = text("select * from cool_review")
        res3 = session.execute(query3)
        res3_df = toDataFrame(res3)
        res = {
            'helpful': res1_df.to_dict('records'),
            'funny': res2_df.to_dict('records'),
            'cool': res3_df.to_dict('records')
        }
        res_json = jsonify(res)
        return res_json


@review_blue.route('/helpful_review')
def helpful_review():
    with get_session() as session:
        query = text("select * from helpful_review")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


@review_blue.route('/funny_review')
def funny_review():
    with get_session() as session:
        query = text("select * from funny_review")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


@review_blue.route('/cool_review')
def cool_review():
    with get_session() as session:
        query = text("select * from cool_review")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res
