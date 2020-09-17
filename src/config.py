import json


def load_config():
    try:
        with open("/config.json", "r") as config_file:
            return json.load(config_file)
    except ValueError:
        print("Illegal JSON file recieved")
        return {}
