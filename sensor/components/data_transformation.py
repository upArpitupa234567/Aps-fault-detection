from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing  import Optional
import pandas as pd
import os,sys
# from sklearn.preprocessing import Pipeline
from sklearn.pipeline import Pipeline
from sensor import utils 
import numpy as np
# from sklearn.pipeline import LabelEncoder
from sklearn.preprocessing import LabelEncoder


from imblearn.combine import SMOTETomek  # it helps to generate data for minority class  , we can balance our dataset with this library
from sklearn.impute import SimpleImputer # it generates some values for missing values
from sklearn.preprocessing import RobustScaler # it minimize the outlier , Robustscaler is just like StandardScaler
from sensor.config import TARGET_COLUMN



class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    #instance means each object we are creating from a class that is completely isolated  from other object
    #but when we are saying this is class method that means this is share with across all objects
    #means whenever we have something we wants to share with each and every object then we can declare that as class method 
    
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy="constant",fill_value=0)
            robust_scaler = RobustScaler() #Robust sacler will handle the outliers

            pipeline = Pipeline(steps=[
                ('Imputer',simple_imputer),
                ('RobustScaler',robust_scaler)
            ])
        
            return pipeline

        except Exception as e:
            raise SensorException (e, sys)
    
    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting input feature for train and test dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)
            
            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr =  label_encoder.transform(target_feature_test_df)

            exclude_columns = [TARGET_COLUMN]
            # base_df = utils.convert_columns_float(df=base_df,exclude_columns=exclude_columns)
            # train_df = utils.convert_columns_float(df=train_df,exclude_columns=exclude_columns)
            # test_df = utils.convert_columns_float(df=test_df,exclude_columns=exclude_columns)
            input_feature_train_df = utils.convert_columns_float(df=input_feature_train_df, exclude_columns=exclude_columns)
            input_feature_test_df = utils.convert_columns_float(df=input_feature_test_df, exclude_columns=exclude_columns)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)
            
            #transfrom input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            smt = SMOTETomek(sampling_strategy="minority")
            logging.info(f"Before resampling in training set input{input_feature_train_arr.shape} Target:{target_feature_train_arr}")
            input_feature_train_arr ,target_feature_train_arr= smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling in training set input{input_feature_train_arr.shape} Target:{target_feature_train_arr}")

            logging.info(f"Before resampling in testing set input{input_feature_test_arr.shape} Target:{target_feature_test_arr}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After resampling in testing set input{input_feature_test_arr.shape} Target:{target_feature_test_arr}")

            #target encoder
            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]

            #save numpy array
            utils.save_numpy_arr_data(file_path=self.data_transformation_config.transformed_train_path,
                                      array=train_arr)
            
            utils.save_numpy_arr_data(file_path=self.data_transformation_config.transformed_test_path,
                                      array=test_arr)
            
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
                              obj = transformation_pipeline)
            
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
                              obj=label_encoder)
            

            Data_transformation_artifact  = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path
            )

            logging.info(f"Data transformation object {Data_transformation_artifact}")
            return Data_transformation_artifact


        except Exception as e:
            raise SensorException (e, sys)
