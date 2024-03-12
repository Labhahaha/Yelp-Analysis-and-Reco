from flask import Blueprint

# 创建蓝图
filter_blue = Blueprint('filter', __name__)

# 按距离筛选商家
def filter_by_distance(filter_condition, df):
    filter_df = df
    # 不足1km
    if filter_condition == "(0,1)":
        filter_df = filter_df[(filter_df["distance"] >= 0) & (filter_df["distance"] < 1000)]


    # 1~2km
    elif filter_condition == "(1,2)":
        filter_df = filter_df[(filter_df["distance"] >= 1000) & (filter_df["distance"] < 2000)]


    # 2~5km
    elif filter_condition == "(2,5)":
        filter_df = filter_df[(filter_df["distance"] >= 2000) & (filter_df["distance"] < 5000)]

    # 超过5km
    elif filter_condition == "(5,n)":
        filter_df = filter_df[filter_df["distance"] >=5000]

    return filter_df


# 按星级评分筛选商家
def filter_by_stars(filter_condition,df):
    # 五星商家
    if filter_condition == "five_stars":
        filter_df = df[df["stars"] == 5]

    # 四星及以上商家
    elif filter_condition == "more_than_four_stars":
        filter_df = df[df["stars"] >= 4]

    # 三星及以上商家
    elif filter_condition == "more_than_three_stars":
        filter_df = df[df["stars"] >= 3]

    return filter_df

def filter(df,filter_type,filter_condition):

    result_df = df
    if filter_type == "distance":
        result_df = filter_by_distance(filter_condition, df)
    elif filter_type == "stars":
        result_df = filter_by_stars(filter_condition,df)
    elif filter_type == "facilities":
        pass
    else:
        pass

    return result_df