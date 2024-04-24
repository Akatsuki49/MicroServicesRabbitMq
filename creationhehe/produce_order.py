import pika
import json

# RabbitMQ connection parameters
rabbitmq_host = "localhost"
rabbitmq_port = 5672
rabbitmq_queue = "item_creation"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

def publish_item(item_data):
    """
    Publishes the item data to the RabbitMQ queue.
    """
    message = json.dumps(item_data)
    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_queue,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2))  # Make the message persistent
    print(f"Published item: {item_data}")