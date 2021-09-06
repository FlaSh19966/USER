

from pymongo import MongoClient
KEY = "super-secret"
uri = "mongodb+srv://m220student:m220password@mflix.ewyk5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db = MongoClient(uri)["sample_users"]


def get_auth(email, password):
    return db.users.find_one({"email": email, "password": password})


def create_session(email, access_token):
    return db.sessions.insert_one({"email": email, "jwt": access_token})


def remove_session(email):
    return db.sessions.delete_one({"email": email})
