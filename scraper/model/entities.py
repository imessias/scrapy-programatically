from pony.orm import *
from pony.orm import Database as PonyDatabase


class Database:
    def __init__(self, **db_params):
        self.model = PonyDatabase(**db_params)

        class Author(self.model.Entity):
            id = PrimaryKey(int, auto=True),
            name = Required(str, unique=True),
            birthdate = Optional(str),
            bio = Optional(str)

        class Quote(self.model.Entity):
            id = PrimaryKey(int, auto=True),
            text = Required(str, unique=True),
            author = Required(str),
            #tags = Set(str)
