from pymongo import MongoClient
import os

client = MongoClient(os.getenv("DATABASE_URL"))
db = client[str(os.getenv("DATABASE_NAME"))]

#print("Database URL connect: " + os.getenv("DATABASE_URL"))
#print("Database Name: " + os.getenv("DATABASE_NAME"))