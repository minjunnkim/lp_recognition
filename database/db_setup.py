from pymongo import MongoClient

def get_database():
    client = MongoClient('mongodb+srv://ckandrew04:2pz6rSymbmXPBpVP@evcharging.i3nxnwz.mongodb.net/?retryWrites=true&w=majority&appName=evcharging')
    return client['ev_charging']

def create_profiles_collection(db):
    db.create_collection('profiles')

if __name__ == "__main__":
    db = get_database()
    create_profiles_collection(db)