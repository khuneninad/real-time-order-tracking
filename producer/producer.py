from kafka import KafkaProducer
import json, time
from order_generator import generate_order

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode()
)

order_id = 1

while True:
    data = generate_order(order_id)
    producer.send("order_tracking", data)

    print(data)

    order_id += 1
    time.sleep(0.2)