from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from buy_now import handle_buy_now
from add_test_producer import publish_item
from producer import publish_message

mongo_host = "mongodb"
mongo_port = 27017

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
database = client["Inventory"]

server = Flask(__name__)
server.secret_key = "1234"


@server.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@server.route("/register", methods=["POST", "GET"])
def register():
    error = None
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user_collection = database.get_collection("users")
            user = user_collection.find_one({"username": username})
            if user:
                error = "Username already exists. Please choose another."
            else:
                user_collection.insert_one(
                    {"username": username, "password": password})
                return redirect(url_for("login"))
    except Exception as e:
        error = "An error occurred. Please try again."
    return render_template("register.html", error=error)


@server.route("/login", methods=["POST", "GET"])
def login():
    error = None
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user_collection = database.get_collection("users")
            user = user_collection.find_one(
                {"username": username, "password": password}
            )
            if user:
                session["username"] = username
                session["type"] = "customer"
                return redirect(url_for("home", username=username))

            admin_collection = database.get_collection("admin")
            admin = admin_collection.find_one(
                {"username": username, "password": password}
            )
            if admin:
                session["username"] = username
                session["type"] = "admin"
                return redirect(url_for("inventory", username=username))
            else:
                error = "Incorrect username or password. Please try again."
    except Exception as e:
        print(e)
        error = "An error occurred. Please try again."
    return render_template("login.html", error=error)


@server.route("/home/<username>", methods=["GET", "POST"])
def home(username):
    watches = database.get_collection("watches")
    watch_list = list(watches.find())
    name = username
    user_items_collection = database.get_collection("userItem")
    user_items = list(user_items_collection.find({"user": username}))
    return render_template("home.html", username=name, watches=watch_list, user_items=user_items)


@server.route("/buy_now/<watch_id>/<username>", methods=["GET", "POST"])
def buy_now(watch_id, username):
    return handle_buy_now(watch_id, username)


@server.route("/inventory/<username>", methods=["GET", "POST"])
def inventory(username):
    name = username
    watches = database.get_collection("watches")
    watch_list = list(watches.find())

    if request.method == "POST":
        if "deleteItem" in request.form:
            model = request.form["model"]
            brand = request.form["brand"]
            publish_message("delete", model, brand)

        else:
            model = request.form["model"]
            brand = request.form["brand"]
            stock = request.form["stock"]
            price = request.form["price"]
            itemDescription = request.form["itemDescription"]
            image = "https://images-cdn.ubuy.co.in/6537918bb0cbde4d66135ca0-rolex-oyster-perpetual-41mm-automatic.jpg"

            if "addItem" in request.form:
                item_data = {
                    "model": model,
                    "brand": brand,
                    "stock": stock,
                    "price": price,
                    "itemDescription": itemDescription,
                    "image": image,
                }
                publish_item(item_data)
                print("Item published")
                return redirect(url_for("inventory", username=username))

            elif "updateItem" in request.form:
                publish_message("update", model, brand,
                                stock, price, itemDescription)

        return redirect(url_for("inventory", username=username, watch=watch_list))

    return render_template("inventory.html", username=name, watches=watch_list)


@server.route("/get_active", methods=["GET"])
def get_active():
    try:
        # Prepare the activity data
        activity_data = {
            "server_name": "Producer",
            "status": "active"
        }

        # Return the activity data as a JSON response
        return jsonify(activity_data), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@server.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0')

