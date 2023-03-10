from pymongo import MongoClient
from pymongo.collection import Collection
from pandas import DataFrame

client = MongoClient("localhost", 27017)
collection: Collection = client["mypi"]
