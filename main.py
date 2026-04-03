from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.components.data_validation import DataValidation, DataValidationConfig
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
        logging.info("Data Ingestion Completed")
        print(dataingestion_artifact)

        data_Validation_Config = DataValidationConfig(training_pipeline_config= trainingPipelineCofig)
        data_Validation = DataValidation(data_ingestion_articact= dataingestion_artifact, data_validation_config= data_Validation_Config)
        logging.info("Initiate Data Validation")
        data_Validation_Artifact = data_Validation.initiate_data_validation()
        logging.info('Data Validation Completed')
        print (data_Validation_Artifact)


    except Exception as e:
        raise NetworkSecurityException(e, sys)