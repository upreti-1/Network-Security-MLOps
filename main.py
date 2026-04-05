from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.components.data_validation import DataValidation, DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging_modules.logger import logging
from network_security.components.data_transformation import DataTransformation, DataTransformationConfig
from network_security.components.model_trainer import ModelTainerConfig, ModelTrainer

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

        dataTransformationConfig = DataTransformationConfig(trainingPipelineCofig)
        dataTransformation = DataTransformation(data_validation_artifact= data_Validation_Artifact, data_transformation_config= dataTransformationConfig)
        logging.info('Initiating Data Transformation')
        dataTransformationArtifact = dataTransformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print (dataTransformationArtifact)

        logging.info("Model Training Started")
        model_trainer_config = ModelTainerConfig(trainingPipelineCofig)
        model_trainer = ModelTrainer(modelTrainerConfig= model_trainer_config, dataTransformationArtifact= dataTransformationArtifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training Artifact Created")


    except Exception as e:
        raise NetworkSecurityException(e, sys)