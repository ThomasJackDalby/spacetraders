import time
import datetime
import tabulate
from rich import print
from api import *

CACHE_FOLDER = ".cache"
SYSTEMS_FOLDER = os.path.join(CACHE_FOLDER, "systems")

if not os.path.exists(CACHE_FOLDER): os.mkdir(CACHE_FOLDER)
if not os.path.exists(SYSTEMS_FOLDER): os.mkdir(SYSTEMS_FOLDER)

def register_agent():
    data = register("BEARD5")
    with open("token", "a") as file:
        file.writelines([data["data"]["token"]])

    print(get_status())

response = session.get("https://api.spacetraders.io/v2/systems")
response_json = response.json()
meta = response_json["meta"]

def get_file_path(page):
    return os.path.join(SYSTEMS_FOLDER, f"systems.{page}.json")

# for page in range(1, int(1+meta["total"]/20)):
#     systems_page = get_systems(page)
#     file_path = get_file_path(page)
#     with open(file_path, "w") as file:
#         file.write(json.dumps(systems_page, indent=4))
# print(response_json)

systems = []
for page in range(1, int(1+meta["total"]/20)):
    file_path = get_file_path(page)
    with open(file_path, "r") as file:
        systems += json.load(file)
with open(os.path.join(SYSTEMS_FOLDER, f"systems.json"), "w") as file:
    file.write(json.dumps(systems, indent=4))