from rich import print
from api import *
import tabulate

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
        time.sleep(remaining_seconds + 1)

def ship_summary():
    ships = get_ships()
    data = [[
        ship["symbol"],
        ship["frame"]["symbol"],
        ship["nav"]["waypointSymbol"],
        f'{ship["fuel"]["current"]}/{ship["fuel"]["capacity"]}',
    ] for ship in ships]
    print(tabulate.tabulate(data, headers=["Symbol", "Type", "Location", "Fuel"]))