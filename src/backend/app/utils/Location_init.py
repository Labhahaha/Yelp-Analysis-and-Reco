#根据用户所在城市取一个精确经纬度
def location_init():
    from ..Recommendation.Recommend import business_df

    random_row = business_df.sample(n=1)  # 随机选择一行

    longitude = random_row['longitude'].values[0]  # 获取经度
    latitude = random_row['latitude'].values[0]  # 获取纬度

    user_location = [longitude,latitude]

    return user_location
