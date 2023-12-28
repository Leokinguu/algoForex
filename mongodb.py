import pymongo

# Replace these values with your MongoDB connection details
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")  # MongoDB URI
database_name = "position"  # Replace with your database name
collection_name = "trade"  # Replace with your collection name

# Access or create a database
db = mongo_client[database_name]

# Access or create a collection
collection = db[collection_name]

# Data to be inserted into the collection
def add_trade(data):
    # data_to_insert = {
    #     "name": "John Doe",
    #     "email": "johndoe@example.com",
    #     "age": 30
    # }

    # Inserting a single document into the collection
    insert_result = collection.insert_one(data)

    # Check if the insertion was successful
    if insert_result.inserted_id:
        print("Document inserted with ID:", insert_result.inserted_id)
    else:
        print("Insertion failed")

# Retrieving data from the collection
# For example, finding all documents in the collection
# all_documents = collection.find()

# # Displaying all documents in the collection
# print("All documents in the collection:")
# for document in all_documents:
#     print(document)

# Close the MongoDB connection
