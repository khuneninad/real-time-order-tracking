import random
from datetime import datetime
from faker import Faker
from api_fetch import get_crypto_price, get_weather

fake = Faker()

statuses = ["PLACED", "SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED"]

def generate_order(order_id):
    return {
        "order_id": order_id,
        "customer": fake.name(),
        "location": fake.city(),
        "status": random.choice(statuses),
        "timestamp": str(datetime.now()),
        "price_factor": float(get_crypto_price()),
        "weather": get_weather(),
        "delay": random.randint(0, 10)
    }