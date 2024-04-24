from flask import Flask, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize the MongoDB client and database
client = MongoClient("mongodb://localhost:27017")
database = client["Inventory"]


def handle_buy_now(watch_id, username):
    # Get the watch details from the "watches" collection
    watches_collection = database["watches"]
    user_items_collection = database["userItem"]
    watch = watches_collection.find_one({"_id": ObjectId(watch_id)})

    if watch:
        # Get the user details (e.g., from the session or a separate collection)
        user = username

        # Check if the user already has an entry for this watch
        existing_entry = user_items_collection.find_one({
            "user": user,
            "brand": watch["brand"],
            "model": watch["model"]
        })

        if existing_entry:
            # Update the ChosenStock value
            new_stock = existing_entry["ChosenStock"] + 1
            user_items_collection.update_one(
                {"_id": existing_entry["_id"]},
                {"$set": {"ChosenStock": new_stock}}
            )
            chosen_stock = new_stock
        else:
            # Create a new entry in the userItem collection
            new_entry = {
                "user": user,
                "brand": watch["brand"],
                "model": watch["model"],
                "ChosenStock": 1
            }
            result = user_items_collection.insert_one(new_entry)
            chosen_stock = 1

        # Log the required information
        print(f"Username: {user}")
        print(f"Brand: {watch['brand']}")
        print(f"Model: {watch['model']}")
        print(f"ChosenStock: {chosen_stock}")

        return "Buy Now action completed"
    else:
        return "Watch not found"
