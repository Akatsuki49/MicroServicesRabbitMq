import pika
import time
from threading import Thread
import signal
import sys

# RabbitMQ connection details
rabbit_host = 'localhost'
rabbit_queue = 'health_check_queue'
routing_key = 'health_check_queue.report'

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host))
channel = connection.channel()
channel.exchange_declare(exchange=rabbit_queue, exchange_type="direct")

# Service name (replace with your actual service name)
service_name = 'Service 2'


def publish_health_check():
    while True:
        # Publish a health check message to the queue
        channel.basic_publish(
            exchange=rabbit_queue,
            routing_key=routing_key,
            body=service_name.encode('utf-8')
        )
        print(f"{service_name}: Health check message published")
        time.sleep(10)  # Publish a health check message every 10 seconds


def signal_handler(signal, frame):
    print('Closing RabbitMQ connection and exiting...')
    connection.close()
    sys.exit(0)


# Register signal handler for KeyboardInterrupt
signal.signal(signal.SIGINT, signal_handler)

# Start a separate thread for publishing health check messages
health_check_thread = Thread(target=publish_health_check)
health_check_thread.start()

# Your existing service code goes here
# ...

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Signal handler will handle the KeyboardInterrupt
    pass
