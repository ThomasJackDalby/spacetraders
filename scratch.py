import time
import datetime
import tabulate
from rich import print
from api import *

SYSTEM_HOME = "X1-DF55"
waypoint_hq = "X1-DF55-20250Z"
waypoint_asteroid_field = "X1-DF55-17335A"

SHIP_COMMAND = "DALBINGTON-1"
SHIP_MINING_DRONE = "DALBINGTON-2"
SHIP_PROBE = "DALBINGTON-3"

def download_systems():
    for page in range(1, int(1+5000/20)):
        systems = get_systems(page)
        json_object = json.dumps(systems, indent=4)
        with open("systems.json", "a") as file:
            file.write(json_object)

def get_market_waypoints_in_system(system_symbol):
    system = get_system(system_symbol)
    for waypoint_summary in system["waypoints"]:
        waypoint = get_waypoint(system_symbol, waypoint_summary["symbol"])
        if any(filter(lambda trait: trait["symbol"] == "MARKETPLACE", waypoint["traits"])):
            yield waypoint

def market_summary(system_symbol, waypoint_symbol):
    market = get_waypoint_market(system_symbol, waypoint_symbol)
    print(f"[{waypoint_symbol}] Market")
    print("======================")
    if "tradeGoods" in market:
        if "cacheTime" in market: print(f"Cached @ [{market['cacheTime']}]")
        items = [[
                item.get("symbol", "-"),
                item.get("tradeVolume", "-"),
                item.get("supply", "-"),
                item.get("purchasePrice", "-"),
                item.get("sellPrice", "-"),
            ] 
            for item in market["tradeGoods"]]
        items = sorted(items, key=lambda item: item[0])
        print(tabulate.tabulate(items, headers=["Name", "Amount", "Supply", "Buy", "Sell"]))
    else:
        items = []
        if "exchange" in market: items += [[item.get("symbol", "-"), "Y", "Y"] for item in market["exchange"]]
        if "imports" in market: items += [[item.get("symbol", "-"), "Y", "-"] for item in market["imports"]]
        if "exports" in market: items += [[item.get("symbol", "-"), "-", "Y"] for item in market["exports"]]
        items = sorted(items, key=lambda item: item[0])
        print(tabulate.tabulate(items, headers=["Name", "Imports", "Exports"]))


def item_summary(item_symbol):
    # how to choose the markets?

    for market in 

    print(tabulate.tabulate([], headers=["Market", "Buy", "Sell"]))
