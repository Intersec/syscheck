
from common_database import CommonDatabase

class CollectionDatabase(CommonDatabase):

    def add_value(self, collection, value):
        content = self.load()
        db_changed = False

        if collection not in content.keys():
            content[collection] = [ value ]
            db_changed = True
        else:
            if value not in content[collection]:
                content[collection].append(value)
                db_changed = True

        if db_changed:
            self.save(content)

    def remove_value(self, collection, value):
        content = self.load()
        db_changed = False

        if collection in content.keys():
            try:
                content[collection].remove(value)
                db_changed = True
            except ValueError:
                pass

        if db_changed:
            self.save(content)

    def remove_collection(self, collection):
        content = self.load()
        db_changed = False

        if collection in content.keys():
            content[collection] = []
            db_changed = True

        if db_changed:
            self.save(content)

    def get_values(self, collection):
        content = self.load()

        if collection not in content.keys():
            values = []
        else:
            values = content[collection]

        return values
