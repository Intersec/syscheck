
from common_database import CommonDatabase

class KeyValueDatabase(CommonDatabase):

    def set_value(self, key, value):
        """Set a value for a key.

        Note: If the key already exists, it's value will be updated.
        """
        content = self.load()

        content[key] = value

        self.save(content)

    def remove_key(self, key):
        content = self.load()
        db_changed = False

        if key in content.keys():
            content[key] = None
            db_changed = True

        if db_changed:
            self.save(content)

    def get_value(self, key):
        content = self.load()

        try:
            value = content[key]
        except KeyError:
            value = None

        return value

    def is_set(self, key):
        content = self.load()

        try:
            value = content[key]
        except KeyError:
            value = None

        result = value != None

        return result
