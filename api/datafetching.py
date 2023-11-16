import gw2api
import json


# Fetches all item ids in the game
def get_items_ids():
    url = gw2api.request_items()
    data = gw2api.fetch_requests([url], 1, 60)
    allItems = json.loads(data[0])
    return allItems

# Fetches detailed info on each item
def get_items_info(items):
    url = gw2api.request_item_details(items)
    data = gw2api.fetch_requests([url], 5, 60)
    itemInfo = json.loads(data[0])
    return itemInfo

# Fetches item prices for each item
def get_item_prices(items):
    url = gw2api.request_prices(items)
    data = gw2api.fetch_requests([url], 5, 60)
    itemPrices = json.loads(data[0])
    return itemPrices