# import pymongo
# client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

# dataBase = client["neurolabDB"]

# collection = dataBase["Products"]

# d = {"companyName":"iNeuron",
#      "product":"Affordable AI",
#      "courseOffered":"Machine Learning with Deployment"
# }

# rec = collection.insert_one(d)

# all_record = collection.find()

# for idx,record in enumerate(all_record):
#     print(f"{idx}: {record}")
    

from sensor.logger import logging
from sensor.exception import SensorException
# from sensor.utils import get_collection_as_dataframe
import sys, os 
from sensor.entity import config_entity
# from sensor.entity.config_entity import DataIngestion
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation

# def test_logger_and_exception():
#     try:
#         result = 3/0 
#         print(result)
#     except Exception as e:
#         raise SensorException(e, sys)
    
if __name__ =="__main__":
    try:
        # test_logger_and_exception()
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        #data ingestion
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        # print(data_ingestion.initiate_data_ingestion())
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()


        #data validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                        data_ingetsion_artifact=data_ingestion_artifact)
        
        data_validation_artifact = data_validation.initiate_data_validation()



        #data transformation
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                 data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()


        #model trainer
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,
                                     data_ingestion_artifact = data_ingestion_artifact,
                                       data_transformation_artifact= data_transformation_artifact,
                                       model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.inititiate_model_evaluation()


    except Exception as e:
        print(e)