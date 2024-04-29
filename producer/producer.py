import pika

# RabbitMQ connection details
rabbit_host = "rabbitmq"
rabbit_exchange = "stock_management_exchange"
rabbit_queue = "stock_management_queue"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,heartbeat=600))
channel = connection.channel()

# Declare the exchange and queue
channel.exchange_declare(exchange=rabbit_exchange, exchange_type="direct")
channel.queue_declare(queue=rabbit_queue)
channel.queue_bind(
    exchange=rabbit_exchange, queue=rabbit_queue, routing_key="stock_management"
)


def publish_message(action, model, brand, stock=None, price=None, itemDescription=None):
    if action == "update":
        message = f"{action},{model},{brand},{stock},{price},{itemDescription}"
    else:
        message = f"{action},{model},{brand}"

    channel.basic_publish(
        exchange=rabbit_exchange, routing_key="stock_management", body=message
    )
    print(f"Sent message: {message}")


# connection.close()
