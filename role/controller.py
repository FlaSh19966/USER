

from master.controller import db


def get_all_roles():
    return db.roles.find({}, {"_id": 0})


def add_role(role):
    return db.roles.insert_one({"role": role})


def remove_role(role):
    return db.roles.delete_one({"role": role})


def update_role(role, new_role):
    return db.roles.update_one({"role": role}, {"$set": {"role": new_role}})


