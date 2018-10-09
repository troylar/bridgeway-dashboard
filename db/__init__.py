from tinydb import TinyDB, Query

class DbManager:
    def __init__(self, **kwargs):
        self.db_path = kwargs.get('DbPath', './db.json')
        self.db = TinyDB(self.db_path)
