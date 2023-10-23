import pymongo

class DatabaseConnector:
    def __init__(self, db_url, db_name):
        self.client = pymongo.MongoClient(db_url)
        self.database = self.client[db_name]

    def get_collection(self, collection_name):
        return self.database[collection_name]
