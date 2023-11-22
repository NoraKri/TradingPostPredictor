def filter_items_by_category(items, category):
    return items[items["type"] == category]

def dataframe_to_id_list(df):
    return df["id"].tolist()

