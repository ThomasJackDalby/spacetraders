import time
import datetime
import tabulate
from rich import print
from api import get, post

def get_status():
    return get("https://api.spacetraders.io/v2/my/agent")

def get_systems():
    return get("https://api.spacetraders.io/v2/systems")

def get_system(system_symbol):
    return get(f"https://api.spacetraders.io/v2/systems/{system_symbol}")

def get_waypoints(system_symbol = "X1-DF55"):
    return get(f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints/")

def get_waypoint(system_symbol, waypoint_symbol):
    return get(f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints/{waypoint_symbol}")

def get_waypoint_market(system_symbol, waypoint_symbol):
    return get(f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints/{waypoint_symbol}/market")

def get_waypoint_shipyard(system_symbol, waypoint_symbol):
    return get(f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints/{waypoint_symbol}/shipyard")

def get_contracts():
    return get("https://api.spacetraders.io/v2/my/contracts")

def get_ships():
    URL = "https://api.spacetraders.io/v2/my/ships"
    print(get(URL))

def get_ship(ship_symbol):
    url = f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}"
    return get(url)

# actions
def buy_ship(waypoint_symbol = "X1-DF55-69207D", ship_type = "SHIP_MINING_DRONE"):
    return post("https://api.spacetraders.io/v2/my/ships", {
        "shipType" : ship_type,
        "waypointSymbol" : waypoint_symbol
    })

def accept_contract(contract_id = "clhevkj395bacs60dsky9qf5q"):
    return get(f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept")

# commands
def navigate_to(ship_symbol, waypoint_symbol):
    print(f"NAVIGATE [{ship_symbol}] to [{waypoint_symbol}]")
    return post(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate", {
        "waypointSymbol" : waypoint_symbol
    })

def dock_ship(ship_symbol):
    print(f"DOCK [{ship_symbol}]")
    url = f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/dock"
    return post(url)

def orbit_ship(ship_symbol):
    print(f"ORBIT [{ship_symbol}]")
    url = f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/orbit"
    return post(url)

def refuel_ship(ship_symbol):
    print(f"REFUEL [{ship_symbol}]")
    url = f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/refuel"
    return post(url)

def extract_ship(ship_symbol):
    print(f"EXTRACT [{ship_symbol}]")
    url = f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/extract"
    return post(url)

def deliver_ship(contract_id, ship_symbol, resource_symbol, amount):
    print(f"DELIVER [{ship_symbol}] [{resource_symbol}] (x{amount}) against [{contract_id}]")
    return post(f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/deliver", {
        "shipSymbol" : ship_symbol, 
        "tradeSymbol" : resource_symbol,
        "units": amount
    })

# info
def get_ship_cooldown(ship_symbol):
    return get(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/cooldown")

def get_ship_cargo(ship_symbol):
    return get(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/cargo")

def get_ship_nav(ship_symbol):
    return get(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/nav")

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

print(get_status())