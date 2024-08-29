import pymongo

class MongoConnection():
    mongo_connection = None
    collection = None

    def __init__(self):
        self.mongo_connection = pymongo.MongoClient("mongodb+srv://tiagojjsousa:xEBe54Cyl3VTuVzp@cluster0.fuyfu.mongodb.net/")["my_mongo_db"]
    
    def get_collection(self,collection_name):
        return self.mongo_connection[collection_name]
    def get_db(self):
        return self.mongo_connection