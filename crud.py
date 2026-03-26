from pymongo import MongoClient

def insert(data, collection, many=False):
    if many:
        return collection.insert_many(data)
    return collection.insert_one(data)

def get(collection, value, identifier="_id"):
    return collection.find_one({identifier: value})