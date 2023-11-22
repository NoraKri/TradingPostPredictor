import datafetching, datetime, json
import pandas as pd
from google.cloud import storage
import os

os.environ.setdefault("GCLOUD_PROJECT", "disco-sky-405321")


class BlobStorage:
    client = storage.Client()
    bucket = client.get_bucket('gw2pricedata-dump')

    item_description_location = "items/item_description/"

    armor_loc = "items/armor/"
    back_loc = "items/back/"
    bag_loc = "items/bag/"
    consumable_loc = "items/consumable/"
    container_loc = "items/container/"
    crafting_material_loc = "items/crafting_material/"
    gathering_loc = "items/gathering/"
    mini_pet_loc = "items/mini_pet/"
    power_core_loc = "items/power_core/"
    trinket_loc = "items/trinket/"
    upgrade_component_loc = "items/upgrade_component/"
    weapon_loc = "items/weapon/"


def read_file(location, name):
    blobs = BlobStorage.bucket.list_blobs(prefix=location)
    matching_blobs = [blob for blob in blobs if name in blob.name]
    result_list = {}
    for blob in matching_blobs:
        data = json.loads(blob.download_as_string(client=None))
        result_list = result_list | data
    df = pd.DataFrame(result_list["data"])
    return df


def get_latest_timestamp(files):
    # Extract the latest timestamp from the list of files
    timestamps = [datetime.datetime.strptime(file.split(' ')[1], "%Y-%m-%dT%H_%M_%S") for file in files]
    return max(timestamps) if timestamps else None

def upload_file(location, name, data):
    json_items = {"data": data}
    BlobStorage.bucket.blob(
        location + name + " " + datetime.datetime.now().strftime('%Y-%m-%dT%H_%M_%S')).upload_from_string(
        data=json.dumps(json_items), content_type='application/json')


def fetch_item_info_and_write_file():
    all_items = datafetching.get_items_ids()
    item_info = datafetching.get_items_info(all_items)
    upload_file(BlobStorage.item_description_location, "item_description", item_info)


def fetch_all_history_and_write_file(location, ids):
    # First, check if location is empty, if no, then fetch only the history from the last recorded timestamp in the location
    blobs = BlobStorage.bucket.list_blobs(prefix=location)
    latest_timestamp = get_latest_timestamp(blobs)
    for item in ids:
        item_data = datafetching.get_item_history(item, latest_timestamp)
        upload_file(location, str(item), item_data)
