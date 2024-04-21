import pymongo
import pandas as pd
import json

client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

# DATA_FILE_PATH =  
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"

if __name__ == "__main__":
    df = pd.read_csv("aps_failure_training_set1.csv")
    print(f"rows and column: {df.shape}")

    #convert dataframe to json so that we can dump these record in mongo db
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())  # T means transpose whole data, rows in column , and column in rows
    print(json_record[0])

    #insert converted json record to mongo db
    # client[DATABASE_NAME][COLLECTION_NAME].delete_many({})
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)