import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("order.notify")
queue_name = queue.method.queue

channel.queue_bind(
    exchange="order",
    queue=queue_name,
    routing_key="order.notify",
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(" [x] Received Notify {}".format(payload.get("user_email")))
    print(payload.get("id"))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)
print(" [*] Waiting for notify messages. To exit press CTRL+C")

channel.start_consuming()
