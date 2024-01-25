
import json
import os

class CommonDatabase():

    def __init__(self, db_path):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as file:
                file.write("{}")

    def save(self, content):
        with open(self.db_path, "w") as f:
            json.dump(content, f)

    def load(self):
        def read_file(filename):
            f = open(filename)
            content = f.read()
            f.close()
            return content

        try:
            db_file_content = read_file(self.db_path)
        except FileNotFoundError:
            db_file_content = "{}"

        db_json = json.loads(db_file_content)

        return db_json
