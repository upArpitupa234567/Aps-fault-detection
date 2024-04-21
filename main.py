import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

dataBase = client["neurolabDB"]

collection = dataBase["Products"]

d = {"companyName":"iNeuron",
     "product":"Affordable AI",
     "courseOffered":"Machine Learning with Deployment"
}

rec = collection.insert_one(d)

all_record = collection.find()

for idx,record in enumerate(all_record):
    print(f"{idx}: {record}")
    