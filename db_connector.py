# db_connector.py
import os
from dotenv import load_dotenv
from tinydb import TinyDB
# Import necessary libraries for Firestore and MongoDB as needed

load_dotenv()

DATABASE_TYPE = os.getenv('DATABASE_TYPE')


class DatabaseInterface:
    def insert(self, data):
        raise NotImplementedError

    def find_all(self):
        raise NotImplementedError

    def find(self, query):
        raise NotImplementedError

    def update(self, query, update_data):
        raise NotImplementedError

    def delete(self, query):
        raise NotImplementedError


from tinydb import TinyDB, Query
class TinyDBClient(DatabaseInterface):
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def insert(self, data):
        return self.db.insert(data)

    def find_all(self):
        return self.db.all()

    def find(self, query):
        QueryObj = Query()
        return self.db.search(QueryObj.any(query))

    def update(self, query, update_data):
        QueryObj = Query()
        return self.db.update(update_data, QueryObj.any(query))

    def delete(self, query):
        QueryObj = Query()
        return self.db.remove(QueryObj.any(query))

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
class FirestoreClient(DatabaseInterface):
    def __init__(self, collection_name):
        self.db = firestore.Client()
        self.collection = self.db.collection(collection_name)

    def insert(self, data):
        return self.collection.add(data)

    def find_all(self):
        return [doc.to_dict() for doc in self.collection.stream()]

    def find(self, query):
        # Example query: [('name', '==', 'John')]
        docs = self.collection.where(*query).stream()
        return [doc.to_dict() for doc in docs]

    def update(self, doc_id, update_data):
        doc_ref = self.collection.document(doc_id)
        doc_ref.update(update_data)

    def delete(self, doc_id):
        self.collection.document(doc_id).delete()

from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDBClient(DatabaseInterface):
    def __init__(self, db_name, collection_name, db_uri="mongodb://localhost:27017/"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        try:
            result = self.collection.insert_one(data)
            print ("result.inserted_id: ", result.inserted_id)
            print ("result: ", result)
        except PyMongoError as e:
            print(f"Insert operation failed: {e}")
            return None

    def find_all(self):
        try:
            # Retrieve all documents from the collection
            return list(self.collection.find())
        except PyMongoError as e:
            print(f"Find all operation failed: {e}")
            return []

    def find(self, query):
        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Find operation failed: {e}")
            return []

    def update(self, query, update_data):
        try:
            result = self.collection.update_many(query, {'$set': update_data})
            return result.modified_count  # Returns the number of documents modified
        except PyMongoError as e:
            print(f"Update operation failed: {e}")
            return 0

    def delete(self, query):
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count  # Returns the number of documents deleted
        except PyMongoError as e:
            print(f"Delete operation failed: {e}")
            return 0



def get_database_client():
    if DATABASE_TYPE == 'tinydb':
        return TinyDBClient('lead_db.json')
    elif DATABASE_TYPE == 'firestore':
        return FirestoreClient('your_collection_name')
    elif DATABASE_TYPE == 'mongodb':
        return MongoDBClient('facebook_crm', 'leads', os.getenv('MONGODB_URI'))
    else:
        raise ValueError(f"Unsupported database type: {DATABASE_TYPE}")

# This function could be expanded to handle specific database operations if needed
