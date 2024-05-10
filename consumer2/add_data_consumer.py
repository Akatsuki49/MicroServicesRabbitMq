import pika
import json
from pymongo import MongoClient

# RabbitMQ connection parameters
rabbitmq_host = "rabbitmq"
# rabbitmq_host = "localhost"
rabbitmq_port = 5672
rabbitmq_queue = "item_creation"
rabbitmq_exchange = "add_item"

# MongoDB connection parameters
mongo_host = "mongodb"
mongo_port = 27017
mongo_db = "Inventory"
mongo_collection = "watches"

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port,heartbeat=600))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='fanout')

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# Bind the queue to the exchange
channel.queue_bind(exchange=rabbitmq_exchange, queue=rabbitmq_queue)

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]


def publish_message(ch, method, properties, body):
    """
    Callback function to process the received message.
    """
    item_data = json.loads(body)
    item_data["stock"] = int(item_data["stock"])
    item_data["price"] = int(item_data["price"])
    print(f"Received item: {item_data}")

    # Insert or update the item in the MongoDB collection
    result = collection.update_one(
        {"model": item_data["model"], "brand": item_data["brand"]},
        {"$set": item_data},
        upsert=True
    )

    print(f"Item {'updated' if result.modified_count else 'inserted'} in MongoDB")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Start consuming messages
print("Waiting for messages...")
channel.basic_consume(queue=rabbitmq_queue,
                      on_message_callback=publish_message, auto_ack=False)
channel.start_consuming()
