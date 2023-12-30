from pymongo import MongoClient

# Establishing a connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['trades']  # Create or access a database named 'trades'
forex_collection = db['forex_trades']  # Create a collection named 'trade_details'
crypto_collection = db['crypto_trades']

# Inserting trade details into MongoDB
def forex_trade_details(trade_result):
    insert_result = forex_collection.insert_one(trade_result)
    if insert_result.inserted_id:
        print("Forex inserted with ID:", insert_result.inserted_id)
    else:
        print("Forex Insertion failed")

def crypto_trade_details(data):
    insert_result = crypto_collection.insert_one(data)
    if insert_result.inserted_id:
        print("Crypto inserted with ID:", insert_result.inserted_id)
    else:
        print("Crypto Insertion failed")