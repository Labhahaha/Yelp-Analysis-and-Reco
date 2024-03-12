from flask import Blueprint, jsonify, json
from flask import request
from ..utils import get_business_by_city, cal_distance,location_init
from .Filter import filter

search_blue = Blueprint('search', __name__, )

df = None


@search_blue.route('/')
def search():
    query = request.args.get('query')
    if query is None:
        return jsonify({"error": "Missing query parameter"}), 400

    df = get_business_by_city('Abington')

    user_location = location_init(df)

    df['distance'] = df.apply(lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]), axis=1)

    df = df[df['name'].str.contains(query, case=False)]

    sortBy = request.args.get('sortBy')

    if sortBy == 'stars':
        df = df.sort_values(by='stars', ascending=False)

    if sortBy == 'review_count':
        df = df.sort_values(by='review_count', ascending=False)
        print(df)

    if sortBy == 'distance':
        df = df.sort_values(by='distance')

    filter_type = request.args.get('filter')
    filter_condition = request.args.get("filter_condition")

    df = filter(df, filter_type, filter_condition)

    json_res = df.to_json(orient='records')

    return json_res, 200
