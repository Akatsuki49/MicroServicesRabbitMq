import threading
import pika
import time
import signal
import sys

# RabbitMQ connection parameters
rabbitmq_host = "localhost"
rabbitmq_port = 5672
health_check_exchange = "health_check_exchange"
health_check_queue = "health_check_queue"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port,heartbeat=600))
channel = connection.channel()

# Declare the health check exchange
channel.exchange_declare(exchange=health_check_exchange, exchange_type='fanout')

def publish_health_check():
    service_name = 'add_data_consumer'
    while True:
        # Publish a health check message to the exchange
        channel.basic_publish(
            exchange=health_check_exchange,
            routing_key='',
            body=service_name.encode('utf-8')
        )
        print(f"{service_name}: Health check message published")
        time.sleep(10)  # Publish a health check message every 10 seconds

def signal_handler(signal, frame):
    print('Closing RabbitMQ connection...')
    connection.close()
    sys.exit(0)

# Register signal handler for KeyboardInterrupt
signal.signal(signal.SIGINT, signal_handler)

# Start publishing health check messages
publish_health_check_thread = threading.Thread(target=publish_health_check)
publish_health_check_thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted by user")
    connection.close()
    sys.exit(0)