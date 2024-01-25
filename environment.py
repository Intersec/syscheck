import os

from collection_database import CollectionDatabase
from key_value_database import KeyValueDatabase

class Environment():
    def __init__(self, key_value_db, collection_db):
        self.key_value_db = key_value_db
        self.collection_db = collection_db
