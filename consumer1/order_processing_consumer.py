import pika
import time
from pymongo import MongoClient
from threading import Thread
from bson import ObjectId
import signal
import sys

# RabbitMQ connection details
rabbit_host = 'host.docker.internal'
# rabbit_host = 'localhost'
rabbit_exchange = 'order_processing_exchange'
rabbit_queue = 'order_processing'

mongo_host = "host.docker.internal"
mongo_port = 27017

client = MongoClient(mongo_host, mongo_port)
database = client["Inventory"]
watches_collection = database.get_collection("watches")
user_items_collection = database.get_collection('userItem')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host))
channel = connection.channel()

# Declare the exchange and queue
channel.exchange_declare(exchange=rabbit_exchange, exchange_type="direct")
channel.queue_declare(queue=rabbit_queue)
channel.queue_bind(
    exchange=rabbit_exchange, queue=rabbit_queue, routing_key="order_processing"
)


def callback(ch, method, properties, body):
    message = body.decode("utf-8").split(",")
    model = message[0]
    brand = message[1]
    id = ObjectId(message[2])
    user = message[3]
    chosen_stock = message[4]
# Check if the user already has an entry for this watch
    existing_entry = user_items_collection.find_one({
        "user": user,
        "brand": brand,
        "model": model
    })

    if existing_entry:
        # Update the ChosenStock value
        new_stock = existing_entry["ChosenStock"] + 1
        user_items_collection.update_one(
            {"_id": existing_entry["_id"]},
            {"$set": {"ChosenStock": new_stock}}
        )
        chosen_stock = new_stock
    else:
        # Create a new entry in the userItem collection
        new_entry = {
            "user": user,
            "brand": brand,
            "model": model,
            "ChosenStock": 1
        }
        result = user_items_collection.insert_one(new_entry)
        chosen_stock = 1

    # Reduce the stock of the watch by 1
    watches_collection.update_one(
        {"_id": id},
        {"$inc": {"stock": -1}}
    )

    # Log the required information
    print(
        f"Username: {user}, Brand: {brand}, Model: {model}, ChosenStock: {chosen_stock}\n[] Done")


channel.basic_consume(on_message_callback=callback,
                      queue=rabbit_queue, auto_ack=True)
print(" [*] Waiting for notify messages. To exit press CTRL+C")
channel.start_consuming()


# Connect to RabbitMQ
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host=rabbit_host))
# channel = connection.channel()
# channel.exchange_declare(exchange=rabbit_queue, exchange_type="direct")

# # Service name (replace with your actual service name)
# service_name = 'Service 1'


# def publish_health_check():
#     while True:
#         # Publish a health check message to the queue
#         channel.basic_publish(
#             exchange=rabbit_queue,
#             routing_key=routing_key,
#             body=service_name.encode('utf-8')
#         )
#         print(f"{service_name}: Health check message published")
#         time.sleep(10)  # Publish a health check message every 10 seconds


# def signal_handler(signal, frame):
#     print('Closing RabbitMQ connection and exiting...')
#     connection.close()
#     sys.exit(0)


# # Register signal handler for KeyboardInterrupt
# signal.signal(signal.SIGINT, signal_handler)

# # Start a separate thread for publishing health check messages
# health_check_thread = Thread(target=publish_health_check)
# health_check_thread.start()

# # Your existing service code goes here
# # ...

# # Keep the main thread alive
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     # Signal handler will handle the KeyboardInterrupt
#     pass
