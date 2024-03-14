import pandas as pd
from sklearn.cluster import KMeans
from ..utils import cal_distance


#使用 KMeans 聚类将商家按照经纬度聚成若干类，这些类可以代表商圈或区域
def find_business_districts(business_df, n_clusters=10):
    # 使用经纬度进行 KMeans 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    coords = business_df[['latitude', 'longitude']].values
    business_df['district'] = kmeans.fit_predict(coords)
    return business_df

def top_k_districts_by_orders(business_df, k=1):
    district_review_counts = business_df.groupby('district')['review_count'].sum().reset_index()
    top_k_districts = district_review_counts.sort_values(by='review_count', ascending=False).head(k)
    # 返回前 k 个商圈的列表
    return top_k_districts['district'].tolist()

# 根据商家所属的商圈，找出每个商圈内的商家
def get_businesses_in_district(business_df, district_ids):
    # 找出指定商圈的 business_id 列表
    businesses_in_district = business_df[business_df['district'].isin(district_ids)]
    return businesses_in_district

# 示例用法
def location_based_list(user_location,business_df,k=1):
    business_df = find_business_districts(business_df,n_clusters=10)
    top_k_districts = top_k_districts_by_orders(business_df, k)
    businesses_in_district = get_businesses_in_district(business_df,top_k_districts)
    businesses_in_district = businesses_in_district.copy()
    businesses_in_district['distance'] = businesses_in_district.apply(lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]), axis=1)
    businesses_in_district = businesses_in_district[businesses_in_district['distance']/1000<6]
    businesses_in_district = businesses_in_district.sort_values(by='distance', ascending=True).head(20)
    return businesses_in_district





