import os
import requests
import json
import datetime
import time
from rich import print

DEBUG = False

RATE_LIMIT = 0.6
TOKEN = os.getenv('SPACETRADERS_TOKEN')
session = requests.session()
session.headers = {"Authorization": f"Bearer {TOKEN}"}

def record_request(method, url, response_data):
    return
    time_stamp = datetime.datetime.now()
    file_name = time_stamp.strftime("%Y%m%d%H%M%S") + ".json"
    file_path = "./archive/responses/"+file_name
    with open(file_path, "w") as file:
        json_object = json.dumps(response_data, indent=4)
        file.write(json_object)

    relative_file_path = "./responses/"+file_name
    with open("archive/index.html", "r") as file:
        lines = file.readlines()
        lines = lines[:-2] + [f"        <a href=\"{relative_file_path}\">[{time_stamp.strftime('%d/%M/%Y %H:%M:%S')}] {method.ljust(6)} {url}</a><br/>\n"] + lines[-2:]
    
    with open("archive/index.html", "w") as file:
        file.writelines(lines)

def get(url):
    response = session.get(url)
    response_data = response.json()

    record_request("GET", url, response_data)
    time.sleep(RATE_LIMIT)    

    if "data" in response_data:
        return response_data["data"]
    elif "error" in response_data:
        print(response_data["error"])
        return None

def post(url, json=None):
    response = session.post(url, json=json)
    response_data = response.json()

    record_request("POST", url, response_data)
    time.sleep(RATE_LIMIT)    
       
    if "data" in response_data:
        return response_data["data"]
    elif "error" in response_data:
        print(response_data["error"])
        return None
    
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
    return get("https://api.spacetraders.io/v2/my/ships")

def get_ship(ship_symbol):
    return get(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}")

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
    return post(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/dock")

def orbit_ship(ship_symbol):
    print(f"ORBIT [{ship_symbol}]")
    return post(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/orbit")

def refuel_ship(ship_symbol):
    print(f"REFUEL [{ship_symbol}]")
    return post(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/refuel")

def extract_ship(ship_symbol):
    print(f"EXTRACT [{ship_symbol}]")
    return post(f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/extract")

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
