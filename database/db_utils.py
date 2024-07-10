from pymongo import MongoClient

def get_database():
    client = MongoClient('mongodb+srv://ckandrew04:2pz6rSymbmXPBpVP@evcharging.i3nxnwz.mongodb.net/?retryWrites=true&w=majority&appName=evcharging')
    return client['ev_charging']

def insert_profile(db, profile_data):
    profiles = db['profiles']
    profiles.insert_one(profile_data)

def get_profiles(db, license_plate):
    profiles = db['profiles']
    return profiles.find_one({"license_plate": license_plate})