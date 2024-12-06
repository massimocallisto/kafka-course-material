import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json
import os

# MQTT Configuration
# Retrieve environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")  # Default to 'localhost' if not set
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))       # Default to 1883 if not set
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")           # Default to '#' if not set

# Kafka Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")  # Default to 'localhost:9092' if not set
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "mqtt")              # Default to 'mqtt' if not set

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    #linger_ms=10
)


# Callback when the MQTT client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    # Subscribe to all topics
    client.subscribe(MQTT_TOPIC)


# Callback when a message is received
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        print(f"Received MQTT message on topic {msg.topic}: {payload}")
        json_object = json.loads(payload)
        # Send message to Kafka
        #producer.send(KAFKA_TOPIC, {"topic": msg.topic, "message": payload})
        producer.send(KAFKA_TOPIC, value=json_object)
        #producer.flush(timeout = 1)
        print(f"Forwarded message to Kafka topic {KAFKA_TOPIC}")
    except Exception as e:
        print(f"Error processing message: {e}")


# Main function
def main():
    # MQTT Client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Connect to MQTT broker
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start MQTT loop
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
