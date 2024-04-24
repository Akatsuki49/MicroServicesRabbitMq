import pika
import time
from collections import defaultdict
from threading import Thread

# RabbitMQ connection details
rabbit_host = 'localhost'
rabbit_queue = 'health_check_queue'

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host))
channel = connection.channel()
queue = channel.queue_declare(queue=rabbit_queue)
queue_name = queue.method.queue
channel.queue_bind(
    exchange="health_check_queue",
    queue=queue_name,
    routing_key="health_check_queue.report",
)

# Dictionary to store last received time for each service
last_received = defaultdict(float)

# Health check interval (in seconds)
health_check_interval = 10

# Flag to indicate whether the consumer is running
consumer_running = True


def callback(ch, method, properties, body):
    service_name = body.decode('utf-8')
    last_received[service_name] = time.time()
    print(f"Received health check message: {service_name}")


# Start consuming messages from the health check queue
print('Waiting for health check messages. To exit press CTRL+C')


def consume():
    try:
        channel.basic_consume(queue=rabbit_queue,
                              on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted by user")
        global consumer_running
        consumer_running = False


def monitor_health():
    while consumer_running:
        time.sleep(health_check_interval)
        current_time = time.time()
        for service, last_check in last_received.items():
            if current_time - last_check > health_check_interval:
                print(f"Service {service} is unhealthy")


# Start consuming messages from the queue
consume_thread = Thread(target=consume)
consume_thread.start()

# Start monitoring the health of services
monitor_thread = Thread(target=monitor_health)
monitor_thread.start()

# Wait for the threads to finish
consume_thread.join()
monitor_thread.join()

# Close the connection
connection.close()
