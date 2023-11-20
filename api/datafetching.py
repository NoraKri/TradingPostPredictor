import gw2api, datawars2api, json


# Chunk items when fetching data with a lot of parameters, because a 414 error is thrown.
def chunk_items(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Fetches all item ids in the game
def get_items_ids():
    url = gw2api.request_items()
    data = gw2api.fetch_requests([url], 1, 60)
    allItems = json.loads(data[0])
    return allItems


# Fetches detailed info on each item
def get_items_info(items):
    # Endpoint is limited to 200 parameters
    item_chunks = list(chunk_items(items, 200))
    combined_results = []

    for chunk in item_chunks:
        url = gw2api.request_item_details(chunk)
        data = gw2api.fetch_requests([url], 5, 60)
        item_prices = json.loads(data[0])

        combined_results.extend(item_prices)

    return combined_results


# Fetches item prices for each item
def get_item_prices(items):
    url = gw2api.request_prices(items)
    data = gw2api.fetch_requests([url], 5, 60)
    itemPrices = json.loads(data[0])
    return itemPrices

def get_item_history(items):
    url = datawars2api.request_item_history(items)
    data = gw2api.fetch_requests([url], 5, 60)
    itemHistory = json.loads(data[0])
    return itemHistory