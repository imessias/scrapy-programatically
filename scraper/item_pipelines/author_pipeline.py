from flask_injector import inject
from scraper.services.author_service import AuthorService


class AuthorDatabasePipeline(object):
    def __init__(self, author_service: AuthorService):
        self.author_service = author_service

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            author_service=crawler.settings.get("SERVICE")
        )

    def process_item(self, item, spider):
        self.author_service.create_author(item["name"], item["birthdate"], item["bio"])
        return item
