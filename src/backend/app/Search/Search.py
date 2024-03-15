from flask import Blueprint, jsonify, json
from flask import request
from .Filter import filter
from ..Recommendation.Recommend import get_recommendations
from .Order import sort
import pandas as pd
search_blue = Blueprint('search', __name__, )

@search_blue.route('/')
def search():
    query = request.args.get('query')
    sortBy = request.args.get('sortBy')
    filter_type = request.args.get('filter')
    filter_condition = request.args.get("filter_condition")
    if query is None:
        return jsonify({"error": "Missing query parameter"}), 400
    recommend_df = pd.read_json(get_recommendations(query),orient='records')
    sorted_df = sort(recommend_df, sortBy)
    filter_df = filter(sorted_df, filter_type, filter_condition)
    json_res = filter_df.to_json(orient='records')
    return json_res
