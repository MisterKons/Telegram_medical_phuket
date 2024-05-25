import pymongo
import pandas as pd
from pymongo import MongoClient
from Support.credentials import MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['kons_new']  # Database name (will be created if it doesn't exist)
collection = db['clinics']  # Collection name (will be created if it doesn't exist)

# Load the Excel file into a Pandas DataFrame
df = pd.read_excel(r"C:\Users\DELL\Desktop\Hospital "
                   r"Work\telegram_bot\updated_clinics_with_consolidated_types_sub_types.xlsx")

# Function to insert clinic data into MongoDB
def insert_clinic_data(dataframe):
    records = dataframe.to_dict(orient='records')
    collection.insert_many(records)

# Insert data into MongoDB
insert_clinic_data(df)

# Verify that the data has been inserted
for doc in collection.find():
    print(doc)
