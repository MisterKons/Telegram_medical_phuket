import pymongo
import pandas as pd
from pymongo import MongoClient
from credentials import MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['kons_new']
collection = db['clinics']

# Print some documents to verify the fields
print("Sample Documents:")
for doc in collection.find().limit(5):
    print(doc)

# Function to fetch unique values from a specified field
def fetch_unique_values(field_name):
    return collection.distinct(field_name)

# Fetch and store available districts and specialities
districts = fetch_unique_values('District')
specialities = fetch_unique_values('Speciality')
subtypes = fetch_unique_values('Sub_type')


# Print available districts and specialities
# print("Available Districts:", districts)
# print("Available Specialities:", specialities)
print("Available Sup_types:", subtypes)
