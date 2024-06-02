import requests
import time
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Citim opțiunile
with open('/data/options.json') as f:
    options = json.load(f)

# Senzorii specificați
inverter_power_sensor = options.get("inverter_power_sensor")
power_meter_sensor = options.get("power_meter_sensor")
charging_current_sensor = options.get("charging_current_sensor")
maximum_charging_current = options.get("maximum_charging_current")

# URL Home Assistant
base_url = "http://supervisor/core/api/states/"
service_url = "http://supervisor/core/api/services/"

# Funcție pentru obținerea datelor de la senzori
def get_sensor_state(sensor):
    headers = {
        "Authorization": "Bearer " + "YOUR_LONG_LIVED_ACCESS_TOKEN",
        "content-type": "application/json",
    }
    response = requests.get(base_url + sensor, headers=headers)
    if response.status_code == 200:
        return response.json()["state"]
    else:
        return None

# Funcție pentru setarea curentului de încărcare
def set_charging_current(current):
    headers = {
        "Authorization": "Bearer " + "YOUR_LONG_LIVED_ACCESS_TOKEN",
        "content-type": "application/json",
    }
    data = {
        "entity_id": maximum_charging_current,
        "value": current
    }
    response = requests.post(service_url + "number/set_value", headers=headers, json=data)
    return response.status_code == 200

# Funcție principală pentru gestionarea încărcării
def manage_charging():
    while True:
        inverter_power = float(get_sensor_state(inverter_power_sensor))
        power_consumption = float(get_sensor_state(power_meter_sensor))
        charging_current = float(get_sensor_state(charging_current_sensor))

        # Logica pentru gestionarea încărcării (simplificată)
        available_power = inverter_power - power_consumption

        if available_power > 0:
            # Calculăm curentul de încărcare în funcție de puterea disponibilă
            new_charging_current = min(available_power / 230, 32)  # 32A este un exemplu de curent maxim
            set_charging_current(new_charging_current)
            print(f"Available power: {available_power}W. Setting charging current to {new_charging_current}A.")
        else:
            # Dacă nu avem putere disponibilă, setăm curentul la 0
            set_charging_current(0)
            print("No available power. Stopping EV charging...")

        time.sleep(60)

@app.route('/')
def index():
    return jsonify({"message": "EVCC Alternative Add-on is running"})

@app.route('/status')
def status():
    return jsonify({
        "inverter_power": get_sensor_state(inverter_power_sensor),
        "power_consumption": get_sensor_state(power_meter_sensor),
        "charging_current": get_sensor_state(charging_current_sensor)
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    manage_charging()

