# We are writing ETL Pipeline here
import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)

import certifi      # used by python libraries to make a secure http connection
ca = certifi.where()        # certificate authority

import pandas as pd
import numpy as np
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging_modules.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
             pass
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop= True, inplace= True)
            # records = list(json.loads(data.T.to_json()).values())   # This line is outdated
            records = data.to_dict(orient= 'records')                   # Replacing with this line
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def insert_data_to_mongo(self, records, database, collection):
        try:
            self.records = records

            # Step 1: Create client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Step 2: Select database
            self.database = self.mongo_client[database]

            # Step 3: Select collection
            self.collection = self.database[collection]

            # Step 4: Insert data
            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
            
if __name__ == '__main__':
    FILE_PATH = 'Network_Data/phisingData.csv'
    DATABASE = 'PRASHANTai'
    collection = 'NetworkData'
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(FILE_PATH)
    print(records)
    no_of_records = network_obj.insert_data_to_mongo(records, DATABASE, collection)
    print(no_of_records)