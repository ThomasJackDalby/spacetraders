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