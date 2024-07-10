from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv('MONGO_DB_URI') 

def get_database():
    client = MongoClient(URI)
    return client['ev_charging']

def create_profiles_collection(db):
    db.create_collection('profiles')

if __name__ == "__main__":
    db = get_database()
    create_profiles_collection(db)