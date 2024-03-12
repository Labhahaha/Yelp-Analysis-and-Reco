
def location_init(business_df):

    random_row = business_df.sample(n=1)  # ���ѡ��һ��

    longitude = random_row['longitude'].values[0]  # ��ȡ����
    latitude = random_row['latitude'].values[0]  # ��ȡγ��

    user_location = [longitude,latitude]

    return user_location
