
from master.controller import db
from bson.objectid import ObjectId


def get_all_users():
    return db.users.find({}, {"_id": 0})


def add_user(user_info, role_id):
    new_user = {
        "name": user_info["name"],
        "email": user_info["email"],
        "password": user_info["password"],
        "role": user_info["role"],
        "role_id": role_id["_id"]
    }
    return db.users.insert_one(new_user)


def update_password(email, new_password):
    return db.users.update_one({"email": email}, {"$set": {"password": new_password}})


def remove_user(email):
    return db.users.delete_one({"email": email})


def get_auth(email, password):
    return db.users.find_one({"email": email, "password": password})


def get_role_id(role):
    return db.roles.find_one({"role": role}, {"_id": 1})


def create_session(email, access_token):
    return db.sessions.insert_one({"email": email, "jwt": access_token})


def remove_session(email):
    return db.sessions.delete_one({"email": email})
