import os
import sys
import json
from pymongo import MongoClient
from bson import ObjectId

# from dotenv import load_dotenv

# load_dotenv()
# Create a file called update_output.md
with open("update_output.md", "w") as file:
    # Redirect standard output to the file
    sys.stdout = file

# Connect to the MongoDB database
client = MongoClient(os.getenv("MONGO_URI"))
db = client["filmset-lighting-library"]


def update_entry(data, data_type):

    collection = db[data_type]
    name = data["Name"]
    # Find the entry in the collection based on the pull request number
    entry = collection.find_one({"Name": name})

    if entry:
        # Convert the id to ObjectId
        data["_id"] = ObjectId(data["_id"])
        # Update the entry with the new data
        collection.update_one({"_id": entry["_id"]}, {"$set": data})
        print(f"Entry for {name} updated successfully.")
    else:
        # Create a new entry with the provided data
        collection.insert_one(data)
        print(f"New entry for {name} created successfully.")
        new_entry_id = collection.find_one({"Name": name})["_id"]
        print(f"ID of the new entry: {new_entry_id}")
        add_id(path, new_entry_id)


def add_id(path, id):
    with open(path, "r") as file:
        data = json.load(file)
    data["_id"] = str(id)
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def get_data(path):
    with open(path) as file:
        json_data = json.load(file)
    return json_data


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_db.py <path_to_json_file> <data_type>")
        sys.exit(1)

    path = sys.argv[1]
    data_type = sys.argv[2]


    data = get_data(path)
    update_entry(data, data_type)

    # Restore standard output
    sys.stdout = sys.__stdout__
