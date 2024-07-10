from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv('MONGO_DB_URI') 

def get_database():
    client = MongoClient(URI)
    return client['ev_charging']

def insert_profile(db, profile_data):
    profiles = db['profiles']
    profiles.insert_one(profile_data)

def get_profiles(db, license_plate):
    profiles = db['profiles']
    return profiles.find_one({"license_plate": license_plate})