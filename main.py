import time
import datetime
import tabulate
from rich import print
from api import *

# scripts
def print_ship_cargo(ship_symbol):
    data = get_ship_cargo(ship_symbol)
    current_capacity = data["units"]
    total_capacity = data["capacity"]
    print(f"[{ship_symbol}] Cargo ({current_capacity}/{total_capacity})")
    print(tabulate.tabulate([[item["symbol"], item["units"]] for item in data["inventory"]], headers=["Item", "Amount"]))

def wait_for_cooldown(ship_symbol):
    data = get_ship_cooldown(ship_symbol)
    remaining_seconds = data["remainingSeconds"]
    if remaining_seconds > 0:
        print(f"AWAITING COOLDOWN -- ETA {remaining_seconds} seconds...")
        time.sleep(remaining_seconds + 1)

def wait_for_arrival(ship_symbol):
    data = get_ship_nav(ship_symbol)
    arrival_time = datetime.datetime.strptime(data["route"]["arrival"], "%Y-%m-%dT%H:%M:%S.%fZ")
    remaining_seconds = (arrival_time - datetime.datetime.utcnow()).total_seconds() + 1
    if remaining_seconds > 0:
        print(f"AWAITING ARRIVAL @ [{data['route']['destination']['symbol']}] -- ETA {remaining_seconds} seconds...")
        time.sleep(remaining_seconds)

def ship_sell(ship_symbol, resource_symbol, amount):
    print(f"Selling [{ship_symbol}] {resource_symbol} x {amount}")
    url = f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/sell"
    return post(url, {
        "symbol" : resource_symbol,
        "units" : amount
    })

system_home = "X1-DF55"
waypoint_hq = "X1-DF55-20250Z"
waypoint_asteroid_field = "X1-DF55-17335A"
ship_command = "DALBINGTON-1"
ship_drone = "DALBINGTON-2"

# dock_ship(ship_drone)
# ship_sell(ship_drone, "SILVER_ORE", 7)

# get_waypoint(system_home, waypoint_hq)
# get_waypoint_market(system_home, waypoint_hq)

# get_waypoint_market(system_home, waypoint_asteroid_field)
# orbit_ship(ship_drone)
# extract_ship(ship_drone)
# navigate_to(ship_drone, asteroid_field)

# data = get_ship(ship_drone)["data"]
# print(data)
# exit()

def mining():
    while True:
        data = get_ship(ship_drone)
        orbit_ship(ship_drone)

        while data["cargo"]["units"] < (data["cargo"]["capacity"] - 5): # mining
            data = extract_ship(ship_drone)

            print_ship_cargo(ship_drone)

            # print(f"cargo ({data['cargo']['units']}/{data['cargo']['capacity']})")
            wait_for_cooldown(ship_drone)

        if any((item for item in data["cargo"]["inventory"] if item["symbol"] != "ALUMINUM_ORE")):
            dock_ship(ship_drone)
            data = get_ship(ship_drone)
            for item in data["cargo"]["inventory"]:
                if item["symbol"] != "ALUMINUM_ORE":
                    ship_sell(ship_drone, item["symbol"], item["units"])
        
        
        if data["cargo"]["units"] < (data["cargo"]["capacity"] - 5): # mining

            data = navigate_to(ship_drone, waypoint_hq)
            wait_for_arrival(ship_drone)

            dock_ship(ship_drone)
            refuel_ship(ship_drone)

            data = get_ship_cargo(ship_drone)
            item = next((item for item in data["inventory"] if item["symbol"] == "ALUMINUM_ORE"), None)
            deliver_ship("clhevkj395bacs60dsky9qf5q", ship_drone, "ALUMINUM_ORE", item["units"])
            orbit_ship(ship_drone)

            data = navigate_to(ship_drone, waypoint_asteroid_field)
            wait_for_arrival(ship_drone)
            
            dock_ship(ship_drone)
            refuel_ship(ship_drone)

print(get_waypoint(system_home, waypoint_hq))