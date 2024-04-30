import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# env_var = EnvironmentVariable()
# mongo_client = pymongo.MongoClient(env_var)
env_var = EnvironmentVariable()

mongo_uri = env_var.mongo_db_url  # Assuming "mongo_db_url" is your MongoDB connection string

mongo_client = pymongo.MongoClient(mongo_uri)