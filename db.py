from pymongo import MongoClient
from pymongo.collection import Collection

client = MongoClient("localhost", 27017)
collection: Collection = client["mypi"]
