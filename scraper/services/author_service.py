from flask_injector import inject
from pony.orm import db_session
from scraper.model.entities import Database


class AuthorService:

    @inject
    def __init__(self, db: Database):
        self.db = db

    @db_session
    def create_author(self, name, birthdate, bio):
        entry = self.db.model.Author.get(lambda s: s.name == name)
        if entry is None:
            author = self.db.model.Author(name=name, birthdate=birthdate, bio=bio)
            return author.to_dict()
        return None

    @db_session
    def list(self):
        authors = self.db.model.Author.select()
        author_list = [author.to_dict() for author in authors]
        return author_list
