from pymongo import MongoClient
import os 

url=os.getenv("MONGO_URL")
client = MongoClient(url)
db = client["core"]
