from rich import print
from api import *
from common import *

# flies to different markets to get the prices
# it's a bit of a traveling sales man..
# fly to closest that we've not done? like a random walk?

DRONE_SYMBOL = "BEARD5-2"

def fly_to_next_market(market_symbol):

    navigate_to(DRONE_SYMBOL, market_symbol)
    wait_for_arrival(DRONE_SYMBOL)





# while True:

#     # get next nearest, un-cached market?

