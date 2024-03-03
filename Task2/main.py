import argparse

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://mdsuser:567234@cluster0.ansi3ze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    # client.admin.command('ping')
    # print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.mds
except Exception as e:
    print(e)

parser = argparse.ArgumentParser(description="Application cats")
parser.add_argument("--action", help="create, update, read, delete")
parser.add_argument("--id", help="id")
parser.add_argument("--name", help="name")
parser.add_argument("--age", help="age")
parser.add_argument("--features", help="features", nargs="+")

args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]


def read():
    return db.cats.find()

def create(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.insert_one(cat)

def update(pk, name, age, features):
    new_cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.update_one({"_id": ObjectId(pk)}, {"$set": new_cat})

def update_features(pk, features):
    new_cat = {
        "features": {"$each": features}
    }
    return db.cats.update_one({"_id": ObjectId(pk)}, {"$push": new_cat})

def update_age(pk, age):
    new_cat = {
        "age": age,
    }
    return db.cats.update_one({"_id": ObjectId(pk)}, {"$set": new_cat})

def delete():
    return db.cats.delete_one({"_id": ObjectId(pk)})

def read_by_name(name=None):
    if not name:
        name = input("Enter name: ")
    document = db.cats.find_one({"name": name})
    if document is not None:
        return document
    else:
        return None

if __name__ == "__main__":
    match action:
        case "read":
            results = read()
            [print(cat) for cat in results]
        case "create":
            result = create(name, age, features)
            print(result)
        case "update":
            result = update(pk, name, age, features)
            print(result)
        case "update_features":
            doc = read_by_name(name)
            pk = doc["_id"]
            result = update_features(pk, features)
            print(result)
        case "update_age":
            doc = read_by_name(name)
            pk = doc["_id"]
            result = update_age(pk, age)
            print(result)
        case "delete":
            doc = read_by_name()
            pk = doc["_id"]
            result = delete()
            print(result)
        case "delete_all":
            results = read()
            for cat in results:
                pk = cat["_id"]
                del_res = delete()
                print(del_res)
        case "read_by_name":
            result = read_by_name()
            print(result)
        case _:
            print("Unknown command")
