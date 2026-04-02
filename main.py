from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging_modules.logger import logging

if __name__ == '__main__':
    try:
        trainingPipelineCofig = TrainingPipelineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingPipelineCofig)
        dataingestion = DataIngestion(dataIngestionConfig)
        logging.info("Initiating Data Ingestion")
        dataingestion_artifact = dataingestion.initiate_data_ingestion()
        print(dataingestion_artifact)
        

    except Exception as e:
        raise NetworkSecurityException(e, sys)