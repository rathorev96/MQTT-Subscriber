import paho.mqtt.client as mqtt
import json

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe("network/topology", qos=1)  # Adjust the topic as needed

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")
    # Save received message to a JSON file
    try:
        data = json.loads(msg.payload.decode())
        with open('received_topology_data.json', 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        print("Data saved to received_topology_data.json")
    except Exception as e:
        print(f"Failed to save data to JSON file: {e}")

# Callback when the client subscribes to a topic
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: {str(mid)} with QoS {str(granted_qos)}")

# Callback for logging
def on_log(client, userdata, level, buf):
    print("log: ", buf)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log  # Uncomment to enable logging

# Connect to the MQTT broker
mqttc.connect("localhost", 1883, 60)  # Update with your broker's address and port

mqttc.loop_forever()
