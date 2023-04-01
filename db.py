from pymongo import MongoClient
import pymongo
from pymongo.collection import Collection

client = pymongo.MongoClient(
    "mongodb+srv://baru:DfCUcKcTigiSDIzD@cluster0.wnrwksk.mongodb.net/?retryWrites=true&w=majority"
)
collection: Collection = client["mypi"]
