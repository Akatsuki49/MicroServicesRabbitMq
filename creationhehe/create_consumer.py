import pika
import json
from pymongo import MongoClient

# RabbitMQ connection parameters
rabbitmq_host = "localhost"
rabbitmq_port = 5672
rabbitmq_queue = "item_creation"

# MongoDB connection parameters
mongo_host = "localhost"
mongo_port = 27017
mongo_db = "Inventory"
mongo_collection = "watches"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

def callback(ch, method, properties, body):
    """
    Callback function to process the received message.
    """
    item_data = json.loads(body)
    print(f"Received item: {item_data}")

    model = item_data["model"]
    brand = item_data["brand"]
    stock = item_data["stock"]
    price = item_data["price"]
    description = item_data["description"]
    image = item_data["image"]

    # Insert the item in the MongoDB collection
    collection.insert_one({
        "model": model,
        "brand": brand,
        "stock": stock,
        "price": price,
        "description": description,
        "image": image,
    })

    print("Item inserted in MongoDB")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages
print("Waiting for messages...")
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=False)
channel.start_consuming()