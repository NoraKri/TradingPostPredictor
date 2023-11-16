import gw2api
import json

def get_items_ids():
    url = gw2api.request_items()
    data = gw2api.fetch_requests([url],1,60)
    allItems = json.loads(data[0])
    return allItems

print(get_items_ids())