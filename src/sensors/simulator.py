import paho.mqtt.client as mqtt
import json
import time
import random

client = mqtt.Client(transport="websockets")  # ✅ Use WebSocket transport
client.connect("broker.hivemq.com", 8000)     # ✅ Port 8000 for WS instead of 1883

def simulate_data():
    while True:
        payload = {
            "soil_moisture": random.randint(30, 70),
            "temperature": round(random.uniform(25, 35), 2)
        }
        client.publish("agriguru/simulated", json.dumps(payload))
        print("Sent:", payload)
        time.sleep(5)

if __name__ == '__main__':
    simulate_data()
