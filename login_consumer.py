import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("login.notify")
queue_name = queue.method.queue

channel.queue_bind(
    exchange="login",
    queue=queue_name,
    routing_key="login.notify",
)

def callback(ch, method, properties, body):
    payload = json.loads(body)
    username = payload.get("username")
    login_time = payload.get("login_time")
    print(" [x] Received Notify - Username: {}, Login Time: {}".format(username, login_time))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_consume(on_message_callback=callback, queue=queue_name)
print(" [*] Waiting for notify messages. To exit press CTRL+C")
channel.start_consuming()