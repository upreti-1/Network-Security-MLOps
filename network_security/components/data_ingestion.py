from network_security.exception.exception import NetworkSecurityException
from network_security.logging_modules.logger import logging

# Configuration of the Data Ingestion Config
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')


# starting reading form this URL
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        '''
        read data from MongoDB
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            # while retriving data form mongoDB, an column '-id' usually gets added. so removal is important
            if '_id' in df.columns.to_list():
                df = df.drop(columns='_id')

            df.replace({'na':np.nan}, inplace= True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
    def export_data_to_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok= True)
            dataframe.to_csv(feature_store_file_path, index = False, header= True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            
            training_file_path = self.data_ingestion_config.training_file_path
            testing_file_path = self.data_ingestion_config.testing_file_path

            train_set, test_set = train_test_split(
                dataframe, test_size= self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the DataFrame")

            logging.info('Exited split_data_as_train_test method of DataIngestion class')

            os.makedirs(os.path.dirname(training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(testing_file_path), exist_ok=True)

            train_set.to_csv(training_file_path, index=False, header=True)
            logging.info('train set loading completed')

            test_set.to_csv(testing_file_path, index=False, header=True)
            logging.info('test set loading completed')

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            dataingestionartifact = DataIngestionArtifact(train_file_path = self.data_ingestion_config.training_file_path, test_file_path = self.data_ingestion_config.testing_file_path)
            return dataingestionartifact



        except Exception as e:
            raise NetworkSecurityException(e, sys)