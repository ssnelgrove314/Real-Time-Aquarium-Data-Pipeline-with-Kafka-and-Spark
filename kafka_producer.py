import json
import time
from confluent_kafka import Producer
from generate_data import generate_sensor_data  # Importing the data generation function

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "aquarium_sensors"

# Initialize Kafka Producer
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def delivery_report(err, msg):
    """
    Callback function to report message delivery status.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [Partition: {msg.partition()}]")

def main():
    """
    Generates and sends simulated sensor data to Kafka.
    """
    while True:
        # Get simulated data from the external script
        data = generate_sensor_data()
        data_json = json.dumps(data)
        
        # Send data to Kafka
        producer.produce(KAFKA_TOPIC, data_json, callback=delivery_report)
        print(f"Produced: {data_json}")
        
        # Ensure delivery and wait before sending the next message
        producer.flush()
        time.sleep(1)

if __name__ == "__main__":
    main()
