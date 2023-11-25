from pymongo import MongoClient
from dotenv import load_dotenv
import os

client = MongoClient(os.getenv("DATABASE_URL"))
db = client[str(os.getenv("DATABASE_NAME"))]