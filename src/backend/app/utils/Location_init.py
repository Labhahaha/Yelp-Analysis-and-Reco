
def location_init(business_df):

    random_row = business_df.sample(n=1)

    longitude = random_row['longitude'].values[0]
    latitude = random_row['latitude'].values[0]

    user_location = [longitude,latitude]

    return user_location
