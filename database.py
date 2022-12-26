from pymongo import MongoClient

client = MongoClient("mongodb+srv://glinsky:5555@cluster0.tiwuk5b.mongodb.net/?retryWrites=true&w=majority")
db = client["glinskyBot"]
users = db["users"]
date = db["date"]