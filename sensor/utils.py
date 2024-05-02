import pandas as pd
from sensor.exception import SensorException
from sensor.config import mongo_client
from sensor.logger import logging
import os,sys 
import yaml
import dill
import numpy as np


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """
    Description:This function return collection as dataframe

    database name : database name
    collection_name : collection name

    =================================================

    return Pandas dataframe of collection
    
    """    
    try:
        logging.info("Reading data from database:{database_name} and collection:{collection_name}" )
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns:{df.columns}")
        if "id" in df.columns:
            logging.info(f"Dropping columns:id")
            df = df.drop("id",axis =1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df

    except Exception as e:
        raise SensorException(e, sys)
    

def write_yaml_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)

        os.makedirs(file_dir, exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data, file_writer)  # this dumpmethod write all the data wjhat we are getting
            # yaml is type of file like json it is more readable 

    except Exception as e:
        raise SensorException(e, sys)
    
# def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
#     try:
#         for column in df.columns:
#             if column not in exclude_columns:
#                 df[column]=df[column].astype("float")
#         return df
#     except Exception as e:
#         raise e

import pandas as pd

def convert_columns_float(df: pd.DataFrame, exclude_columns: list = []) -> pd.DataFrame:
    """
    Converts columns in a DataFrame to float, excluding specified columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
        exclude_columns (list, optional): List of column names to exclude
            from conversion. Defaults to [].

    Returns:
        pd.DataFrame: DataFrame with converted columns.
    """

    for col in df.columns:
        if col not in exclude_columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Handle non-numeric with 'coerce'
            except:  # Catch any exceptions (more specific if possible)
                # Optionally, log a warning here to indicate potential data quality issues
                print(f"Warning: Could not convert column '{col}' to float (possibly non-numeric values).")
    return df

#this func is for saving the object
def save_object(file_path:str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)  # with the help dill library we save the object or model in pkl(pikle) format
        logging.info("Exited the save_object method of MainUtils class")
    
    except Exception as e:
        raise SensorException(e, sys) from e

#this is for loading the object
#for save something we use dill.dump as above code mentioned
#for load something we use dill.laod mention below code

def load_object(file_path: str) ->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    
    except Exception as e:
        raise SensorException(e, sys) from e

def save_numpy_arr_data(file_path: str, array:np.array):
    """
    Save numpy array data to file
    file_path = str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, "wb")as file_obj :
            np.save(file_obj,array)  # np.save means save array to file
    except Exception as e:
        raise SensorException(e, sys) from e
    

def load_numpy_array_data(file_path:str)->np.array:

    """
    load numpy array data from file
    file_path:str location of file to load
    return:np.array data loaded
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e            
