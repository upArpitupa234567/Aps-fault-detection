import pandas as pd
from sensor.exception import SensorException
from sensor.config import mongo_client
from sensor.logger import logging
import os,sys 
import yaml


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

