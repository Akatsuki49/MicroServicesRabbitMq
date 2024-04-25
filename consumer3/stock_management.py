import pika
from pymongo import MongoClient
import time
from threading import Thread
import signal
import sys

# RabbitMQ connection details
rabbit_host = "localhost"
rabbit_exchange = "stock_management_exchange"
rabbit_queue = "stock_management_queue"

# MongoDB connection details
mongo_host = "localhost"
mongo_port = 27017

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
database = client["Inventory"]
watches = database.get_collection("watches")

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
channel = connection.channel()

# Declare the exchange and queue
channel.exchange_declare(exchange=rabbit_exchange, exchange_type="direct")
channel.queue_declare(queue=rabbit_queue)
channel.queue_bind(
    exchange=rabbit_exchange, queue=rabbit_queue, routing_key="stock_management"
)


def callback(ch, method, properties, body):
    message = body.decode("utf-8").split(",")
    action = message[0]
    model = message[1]
    brand = message[2]

    if action == "update":
        stock = message[3]
        price = message[4]
        itemDescription = message[5]
        update_item(model, brand, stock, price, itemDescription)
    elif action == "delete":
        delete_item(model, brand)


def update_item(model, brand, stock, price, itemDescription):
    watch_exists = watches.count_documents({"model": model, "brand": brand})
    if watch_exists > 0:
        print(f"\nUpdating item {model} with brand {brand}\n")
        watches.update_one(
            {"model": model, "brand": brand},
            {
                "$set": {
                    "stock": int(stock),
                    "price": int(price),
                    "itemDescription": itemDescription,
                    "image": "https://images-cdn.ubuy.co.in/6537918bb0cbde4d66135ca0-rolex-oyster-perpetual-41mm-automatic.jpg",
                }
            },
        )
    else:
        print(f"\nWatch {model} {brand} not found in the database.")


def delete_item(model, brand):
    watch_exists = watches.count_documents({"model": model, "brand": brand})
    if watch_exists > 0:
        print(f"\nDeleting watch {model} {brand} details\n")
        watches.delete_one({"model": model, "brand": brand})
    else:
        print(f"Watch {model} {brand} not found in the database.")


# Start consuming messages
print("Waiting for stock management messages. To exit press CTRL+C")
channel.basic_consume(queue=rabbit_queue, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

# # RabbitMQ connection details
# rabbit_host = 'localhost'
# rabbit_queue = 'health_check_queue'
# routing_key = 'health_check_queue.report'

# # Connect to RabbitMQ
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host=rabbit_host))
# channel = connection.channel()
# channel.exchange_declare(exchange=rabbit_queue, exchange_type="direct")

# # Service name (replace with your actual service name)
# service_name = 'Service 3'


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
