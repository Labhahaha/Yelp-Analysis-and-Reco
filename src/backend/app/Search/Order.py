def sort(df,sortBy):
    if sortBy == 'stars':
        df = df.sort_values(by='stars', ascending=False)
        return df
    elif sortBy == 'review_count':
        df = df.sort_values(by='review_count', ascending=False)
        return df
    elif sortBy == 'distance':
        df = df.sort_values(by='distance')
        return df
    else:
        return df
