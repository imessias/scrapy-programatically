from flask_injector import inject 
from pony.orm import db_session
from scraper.model.entities import Database
import scrapy


class QuoteService:
    @inject
    def __init__(self, db: Database):
        self.db = db

    @db_session
    def create_quote(self, text, author):
        entry = self.db.model.Quote.get(lambda s: s.text == text)
        if entry is None:
            quote = self.db.model.Quote(text, author)
            return quote.to_dict()
        return None

    @db_session
    def list(self):
        quotes = self.db.model.Quote.select()
        quote_list = [quote.to_dict() for quote in quotes]
        return quote_list
