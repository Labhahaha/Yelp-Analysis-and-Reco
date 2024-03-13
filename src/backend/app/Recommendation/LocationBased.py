from ..utils import cal_distance

def get_distance_for_business(user_location,business_df):
    business_df['distance'] = business_df.apply(
        lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]), axis=1)