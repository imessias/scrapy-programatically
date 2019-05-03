from flask_injector import singleton
from injector import Injector
from scraper.model.entities import Database
from scraper.services import SERVICES
from scraper.spiders.author_spider import AuthorSpider
from scraper.scrape import Scraper
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))


def configure(binder):
    PROVIDER = "sqlite"
    FILE_NAME = os.path.join("..", "..", "data", "database.sqlite")
    create_db = True

    args = {
        "provider": PROVIDER,
        "filename": FILE_NAME,
        "create_db": create_db
    }

    db = Database(**args)
    db.model.generate_mapping(create_tables=True)
    binder.bind(Database, to=db, scope=singleton)

    for service in SERVICES:
        binder.bind(service, scope=singleton)
    binder.bind(AuthorSpider)

    binder.bind(Scraper)

injector = Injector(modules=[configure])

if __name__ == "__main__":
    scraper = injector.get(Scraper)
   # for service in SERVICES:
   #     service.get_list()
