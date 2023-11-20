from urllib.request import Request

try:
    import json
except ImportError:
    import simplejson as json


class DATAWARS2API:
    V1 = 'v1'
    V2 = 'v2'
    BaseUrl = 'https://api.datawars2.ie/gw2/'


def _request(gw2api_version, json_location, **args):
    # Makes a request on the Guild Wars 2 API.
    url = DATAWARS2API.BaseUrl + gw2api_version + '/' + json_location + '?' + '&'.join(
        str(argument) + '=' + str(value) for argument, value in args.items() if argument != 'authorization')
    print(url)
    req = Request(url)
    if 'authorization' in args:
        req.add_header('authorization', args['authorization'])
    return req


def request_item_history(ids):
    # Creates a request to get the price history of a list of items.
    return _request(DATAWARS2API.V2, 'history/json', itemID=','.join(str(id) for id in ids))


