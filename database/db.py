from pymongo import MongoClient
import os

client = MongoClient(os.getenv("DATABASE_URL"))
db = client[str(os.getenv("DATABASE_NAME"))]