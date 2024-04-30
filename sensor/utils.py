import pandas as pd
from sensor.exception import SensorException
from sensor.config import mongo_client
from sensor.logger import logging
import os,sys


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
