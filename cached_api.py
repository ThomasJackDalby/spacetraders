import api
import os
import json
import datetime

CACHE_FOLDER_NAME = ".cache"

def _get_file_name(keys):
    return f"{'.'.join(keys)}.json"

def _get_file_path(url_key, keys):
    file_name = _get_file_name(keys)
    return os.path.join(CACHE_FOLDER_NAME, url_key, file_name)

def _write(file_path, data):
    with open(file_path, "w") as file:
        file.write(json.dumps({
            "cacheTime": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "data": data
        }, indent=4))

def _read(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return json.load(file)["data"]

def get_keys()

def get_waypoint_market(system_symbol, waypoint_symbol, use_cache=True):
    file_path = _get_file_path("get_waypoint_market", [system_symbol, waypoint_symbol])
    folder_path = os.path.join(CACHE_FOLDER_NAME, "get_waypoint_market")
    if not os.path.exists(folder_path): 
        os.mkdir(folder_path)

    if use_cache and os.path.exists(file_path):
        return _read(file_path)

    print("Using API")
    data = api.get(f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints/{waypoint_symbol}/market")
    _write(file_path, data)
    return data

# file_path = f".cache/{waypoint_symbol}.market.json"
#     if "tradeGoods" in data:
#         with open(file_path, "w") as file:
#             file.write(json.dumps({
#                 "cacheTime": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#                 "tradeGoods": data["tradeGoods"]
#             }, indent=4))
#     elif allow_cache and os.path.exists(file_path):
#         with open(file_path, "r") as file:
#             data.update(json.load(file))
#     return data