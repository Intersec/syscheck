from key_value_database import KeyValueDatabase

class KeyValueVolatileDatabase(KeyValueDatabase):

    def __init__(self, db_path = None):
        self.content = {}
        # Don't save nor use the path

    def save(self, content):
        self.content = content

    def load(self):
        return self.content
