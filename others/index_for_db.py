from pymongo import MongoClient
from Support.credentials import MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['kons_new']
collection = db['clinics']

# Create indexes
collection.create_index("district_new")
collection.create_index("type")
collection.create_index("Sub_type")

print("Indexes created successfully.")
