import pika
from flask import Flask, render_template, redirect,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_host = "mongodb"
mongo_port = 27017

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
database = client["Inventory"]


rabbit_host = "rabbitmq"
rabbit_exchange = "order_processing_exchange"
rabbit_queue = "order_processing_queue"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,heartbeat=600))
channel = connection.channel()

channel.exchange_declare(exchange=rabbit_exchange, exchange_type="direct")
channel.queue_declare(queue=rabbit_queue)
channel.queue_bind(
    exchange=rabbit_exchange, queue=rabbit_queue, routing_key="order_processing"
)

def publish_order_message(watch, user, chosen_stock):
    message = f"{watch['model']},{watch['brand']},{watch['_id']},{user},{chosen_stock}"
    channel.basic_publish(
        exchange=rabbit_exchange, routing_key="order_processing", body=message
    )
    print(f"Sent message: {message}")

def handle_buy_now(watch_id, username):
    # Get the watch details from the "watches" collection
    watches_collection = database["watches"]
    watch_list = list(watches_collection.find())
    user_items_collection = database["userItem"]
    watch = watches_collection.find_one({"_id": ObjectId(watch_id)})
    user_items = list(user_items_collection.find({"user": username}))
    if watch:
        # Check if the current stock is at least 1
        if watch["stock"] < 1:
            return redirect(url_for('home', username=username, watch=watch_list))

        publish_order_message(watch,username,1)

        # return "Buy Now action completed"
        return redirect(url_for('home', username=username, watch=watch_list))
    else:
        # return "Watch not found"
        return redirect(url_for('home', username=username, watch=watch_list))
