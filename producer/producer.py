from kafka import KafkaProducer
import json, time
from order_generator import generate_order

def create_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='localhost:29092',
                value_serializer=lambda v: json.dumps(v).encode()
            )
            print("Connected to Kafka ✅")
            return producer
        except Exception as e:
            print("Retrying Kafka connection...", e)
            time.sleep(5)

producer = create_producer()

order_id = 1

while True:
    order = generate_order(order_id)
    producer.send("orders_topic", value=order)
    print("Sent:", order)

    order_id += 1
    time.sleep(2)