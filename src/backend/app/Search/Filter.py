def filter_by_distance(filter_condition, df):
    filter_df = df
    if filter_condition == "1":
        filter_df = filter_df[filter_df["distance"] < 1000]

    elif filter_condition == "2":
        filter_df = filter_df[filter_df["distance"] < 2000]


    elif filter_condition == "5":
        filter_df = filter_df[filter_df["distance"] < 5000]

    return filter_df


def filter_by_stars(filter_condition,df):
    if filter_condition == "5":
        filter_df = df[df["stars"] == 5]

    elif filter_condition == "4":
        filter_df = df[df["stars"] >= 4]

    elif filter_condition == "3":
        filter_df = df[df["stars"] >= 3]

    return filter_df

def filter(df,filter_type,filter_conditions):

    result_df = df

    #遍历筛选条件
    for filter_type, filter_condition in filter_conditions.items():
        if filter_type == "distance":
            result_df = filter_by_distance(filter_condition, result_df)
        elif filter_type == "stars":
            result_df = filter_by_stars(filter_condition, result_df)
        elif filter_type == "facilities":
            pass
        else:
            pass  # 预留其他条件

    return result_df