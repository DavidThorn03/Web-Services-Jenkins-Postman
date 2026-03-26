from pymongo import MongoClient

def connect_to_cluster():
    uri = "mongodb+srv://b00152842_db_user:nsRFgnH3lgRnfmuY@computerproducts.3sldxxz.mongodb.net/?appName=ComputerProducts"

    client = MongoClient(uri)

    db = client['Products']

    collection = db['Products']

    return client, db, collection