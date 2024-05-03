from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os,sys
from xgboost import XGBClassifier
from sensor import utils
from sklearn.metrics import f1_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise e


    def fine_tune(self):
        try:
            #write code for Grid Search CV
            pass
        
        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self,x,y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise e

    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test array.")
            x_train, y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test, y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model.")
            model = self.train_model(x=x_train, y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)

            logging.info(f"train score : {f1_train_score} and test_score: {f1_test_score}")
            #check for underfitting or overfitting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                                 expected accuracy: {self.model_trainer_config.expected_Score}: model actual score :{f1_test_score}")
            
            logging.info(f"Checking if our model is overfitting or not")
            diff = abs(f1_train_score-f1_test_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than Overfitting threshold {self.model_trainer_config.overfitting_threshold}")
            
            #save the trained model
            logging.info(f"Saving the model obejct")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj = model)

            #prepare artifact
            logging.info("Prepare the artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                                                  f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact


        except Exception as e:
            raise e
            