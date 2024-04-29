# import pika
# import json

# # RabbitMQ connection parameters
# rabbitmq_host = "localhost"
# rabbitmq_exchange="add_item"
# rabbitmq_port = 5672
# rabbitmq_queue = "item_creation"

# # Connect to RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
# channel = connection.channel()

# # Declare the queue
# channel.queue_declare(queue=rabbitmq_queue, durable=True)

# def publish_item(item_data):
#     """
#     Publishes the item data to the RabbitMQ queue.
#     """
#     message = json.dumps(item_data)
#     channel.basic_publish(exchange='',
#                           routing_key=rabbitmq_queue,
#                           body=message,
#                           properties=pika.BasicProperties(delivery_mode=2))  # Make the message persistent
#     print(f"Published item: {item_data}")
import pika
import json

# RabbitMQ connection parameters
rabbitmq_host = "rabbitmq"
rabbitmq_exchange = "add_item"
rabbitmq_port = 5672
rabbitmq_queue = "item_creation"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port,heartbeat=600))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='fanout')

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# Bind the queue to the exchange
channel.queue_bind(exchange=rabbitmq_exchange, queue=rabbitmq_queue)

def publish_item(item_data):
    """
    Publishes the item data to the RabbitMQ queue.
    """
    message = json.dumps(item_data)
    channel.basic_publish(exchange=rabbitmq_exchange, routing_key='', body=message, properties=pika.BasicProperties(delivery_mode=2))
    print(f"Published item: {item_data}")