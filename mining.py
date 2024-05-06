from rich import print
from api import *
from common import *

def mining(
        ship_symbol, 
        mining_location_symbol,
        contract_delivery_symbol,
        contract_id
    ):
    
    ship_nav = get_ship_nav(ship_symbol)
    if ship_nav["waypointSymbol"] != mining_location_symbol:
        navigate_to(ship_symbol, mining_location_symbol)
        wait_for_arrival(ship_symbol)

    while True:
        data = get_ship(ship_symbol)

        while data["cargo"]["units"] < (data["cargo"]["capacity"] - 5): # mining
            data = extract_ship(ship_symbol)
            print_ship_cargo(ship_symbol)
            wait_for_cooldown(ship_symbol)

        if any((item for item in data["cargo"]["inventory"] if item["symbol"] != "ALUMINUM_ORE")):
            dock_ship(ship_symbol)
            data = get_ship(ship_symbol)
            for item in data["cargo"]["inventory"]:
                if item["symbol"] != "ALUMINUM_ORE":
                    ship_sell(ship_symbol, item["symbol"], item["units"])
                    
        elif data["cargo"]["units"] >= (data["cargo"]["capacity"] - 5): # mining
            dock_ship(ship_symbol)
            refuel_ship(ship_symbol)
            orbit_ship(ship_symbol)

            data = navigate_to(ship_symbol, contract_delivery_symbol)
            wait_for_arrival(ship_symbol)

            dock_ship(ship_symbol)
            refuel_ship(ship_symbol)

            data = get_ship_cargo(ship_symbol)
            item = next((item for item in data["inventory"] if item["symbol"] == "ALUMINUM_ORE"), None)
            deliver_ship(contract_id, ship_symbol, "ALUMINUM_ORE", item["units"])
            orbit_ship(ship_symbol)

            data = navigate_to(ship_symbol, mining_location_symbol)
            wait_for_arrival(ship_symbol)
            
            dock_ship(ship_symbol)
            refuel_ship(ship_symbol)
            orbit_ship(ship_symbol)

mining(
    "DALBINGTON-2",
    "X1-DF55-17335A",
    "X1-DF55-20250Z",
    "clhevkj395bacs60dsky9qf5q"
    )