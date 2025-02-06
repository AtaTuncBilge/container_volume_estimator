import paho.mqtt.client as mqtt
import random

BROKER = "mqtt.eclipse.org"
TOPIC = "container/doluluk"

def on_connect(client, userdata, flags, rc):
    print("📡 Bağlandı!")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"💡 Gelen IoT Verisi: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)

while True:
    sensor_value = random.uniform(50, 500)  # Ağırlık Sensörü (kg)
    client.publish(TOPIC, f"Doluluk: {sensor_value} kg")
