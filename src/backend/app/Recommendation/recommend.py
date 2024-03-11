from flask import Blueprint
from ..utils import get_distance
recommend_blue = Blueprint('recommend_blue', __name__)
def get_recommendations():
    recommendations = []