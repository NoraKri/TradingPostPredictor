# gw2api Lampy - Python wrapper for Guild Wars 2 official API.
# Developer: Farshid Hassani Bijarbooneh
# Version 1.3 - 29-07-2015
# Endpoints:
# https://wiki.guildwars2.com/wiki/API:2

from urllib.request import urlopen, Request
from concurrent import futures
import concurrent

try:
    import json
except ImportError:
    import simplejson as json

class GW2API:
    V1 = 'v1'
    V2 = 'v2'
    BaseUrl = 'https://api.guildwars2.com/'


def load_url(url, timeout):
    conn = urlopen(url, timeout=timeout)
    return conn.read()


def _request(gw2api_version, json_location, **args):
    # Makes a request on the Guild Wars 2 API.
    url = GW2API.BaseUrl + gw2api_version + '/' + json_location + '?' + '&'.join(
        str(argument) + '=' + str(value) for argument, value in args.items() if argument != 'authorization')
    print(url)
    req = Request(url)
    if 'authorization' in args:
        req.add_header('authorization', args['authorization'])
    return req


def fetch_requests(requests, max_parallel_requests, timeout):
    # slightly improved version of http://stackoverflow.com/questions/16181121/python-very-simple-multithreading-parallel-url-fetching-without-queue
    with futures.ThreadPoolExecutor(max_workers=max_parallel_requests) as executor:
        # Start the load operations and mark each future with its URL and an index in the call order
        if not isinstance(requests, list):
            requests = [requests]
        data = {}
        req_idx = [i for i in range(len(requests))]
        future_to_url = {executor.submit(load_url, req, timeout): (req, idx) for req, idx in zip(requests, req_idx)}

        for future in concurrent.futures.as_completed(future_to_url):
            (req, idx) = future_to_url[future]
            try:
                data[idx] = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (req, exc))
                # else:
                # print '"%s" fetched data %ss' % (req, data[idx])
        return data

def request_transactions_current_buys(authKey):
    # Creates a request to get the details of the current buy orders
    return _request(GW2API.V2, 'commerce/transactions/current/buys', authorization=authKey)


def request_transactions_current_sells(authKey):
    # Creates a request to get the details of the current sell orders
    return _request(GW2API.V2, 'commerce/transactions/current/sells', authorization=authKey)


def request_transactions_history_buys(authKey):
    # Creates a request to get the details of the history of buy orders
    return _request(GW2API.V2, 'commerce/transactions/history/buys', authorization=authKey)


def request_transactions_history_sells(authKey):
    # Creates a request to get the details of the history of sell orders
    return _request(GW2API.V2, 'commerce/transactions/history/sells', authorization=authKey)



def request_items():
    # Creates a request to get the list of all item ids.
    return _request(GW2API.V2, 'items')


def request_item_details(ids, lang='en'):
    # Creates a request to get the details of a list of items.
    return _request(GW2API.V2, 'items', ids=','.join(str(id) for id in ids), lang=lang)


def request_recipes():
    # Creates a request to get a list of all recipes.
    return _request(GW2API.V2, 'recipes')


def request_recipe_details(ids, lang='en'):
    # Creates a request to get the recipe details of a list of items.
    return _request(GW2API.V2, 'recipes', ids=','.join(str(id) for id in ids), lang=lang)


def request_recipe_search(search_type, id):
    # Creates a request to search for a recipe using input for items as an ingredient
    # and with output for recipes that craft that item.
    s = search_type
    if search_type == 'input':
        return _request(GW2API.V2, 'recipes/search', input=id)
    elif search_type == 'output':
        return _request(GW2API.V2, 'recipes/search', output=id)
    else:
        print("search type mismatch!")


def request_listings(*ids):
    # Creates a request to get the list of all items on TP or listing details of the given item ids.
    if len(ids) < 1:
        return _request(GW2API.V2, 'commerce/listings')
    else:
        return _request(GW2API.V2, 'commerce/listings', ids=','.join(str(id) for id in ids[0]))


def request_prices(*ids):
    # Creates a request to get the list of all items on TP or price details of the given item ids.
    if len(ids) < 1:
        return _request(GW2API.V2, 'commerce/prices')
    else:
        return _request(GW2API.V2, 'commerce/prices', ids=','.join(str(id) for id in ids[0]))


# Sample usage of listings and prices
#
#def test_listings():
#    oneItem = [19684]
#    multipleItems = [19684, 19709, 19970, 19971]
#    req = []
#    req.append(gw2api.request_listings())
#    req.append(gw2api.request_listings(oneItem))
#    req.append(gw2api.request_listings(multipleItems))
#    res = gw2api.fetch_requests(req, 5, TIMEOUT)
#    pprint.pprint(res)
#
#
#def test_prices():
#    oneItem = [19684]
#    multipleItems = [19684, 19709, 19970, 19971]
#    req = []
#    req.append(gw2api.request_prices())
#    req.append(gw2api.request_prices(oneItem))
#    req.append(gw2api.request_prices(multipleItems))
#    res = gw2api.fetch_requests(req, 5, TIMEOUT)
#    pprint.pprint(res)
#
#

def request_exchange(exchange_type, quantity):
    # Creates a request to get the exchange rate for the given quantity of coins or gems.
    if exchange_type == 'coins_to_gems':
        return _request(GW2API.V2, 'commerce/exchange/coins', quantity=quantity)
    elif exchange_type == 'gems_to_coins':
        return _request(GW2API.V2, 'commerce/exchange/gems', quantity=quantity)
    else:
        print("Exchange type mismatch!")
