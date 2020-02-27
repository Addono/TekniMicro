import os
import json

PATH = "src/config.json"

file_exists = os.path.exists(PATH)

with open(PATH, "r+" if file_exists else "w") as config_file:
    try:
        config = json.load(config_file)
    except (json.JSONDecodeError, IOError) as e:
        print(e)
        config = {}

    for field in ['WIFI_SSID', 'WIFI_PASSWORD', 'MQTT_HOSTNAME', 'MQTT_USERNAME', 'MQTT_PASSWORD']:
        if field not in config:
            value = input(f"Please enter the desired value for {field}:\n")
            config[field] = value
    
    # Write the config back to the file
    config_file.seek(0)  # Move the filepointer back to the start, otherwise the new config will be appended
    json.dump(config, config_file)
