import unittest
import os
from flask_injector import singleton
from injector import Injector
from scraper.model.entities import Database
from scraper.services import SERVICES
from scraper.spiders.author_spider import AuthorSpider
from scraper.services.author_service import AuthorService
from scraper.scrape import Scraper
import sys
sys.path.append(os.path.dirname(os.getcwd()))


class AuthorSpiderTest(unittest.TestCase):

    def setUp(self):

        def configure(binder):
            PROVIDER = "sqlite"
            FILE_NAME = os.path.join("..", "..", "data", "database-test.sqlite")
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

        self.injector = Injector(modules=[configure])
        self.db = self.injector.get(Database)
        self.scraper = self.injector.get(Scraper)

    def tearDown(self):
        self.db.model.drop_all_tables(with_all_data=True)

    def testAuthorSpider(self):
        author_service: AuthorService = self.injector.get(AuthorService)

        self.assertTrue(True)
        self.assertIsNotNone(author_service)

        # Getting list of scraped authors #
        authors = author_service.list()
        self.assertIsNotNone(authors)

        # Testing number of entries scraped #
        self.assertTrue(len(authors) == 50)

        # Testing if entries have unique "name" fields #
        for idx, val in enumerate(authors):
            for idx2 in range(idx+1, len(authors)-1):
                self.assertFalse(val["name"] == authors[idx2]["name"])

        # Testing if list has specific elements #
        name = "Albert Einstein"
        birthdate = "March 14, 1879"
        for x in authors:
            if x["name"] == name:
                self.assertEqual(x["birthdate"], birthdate)
                self.assertIsNotNone(x["bio"])
                result = True
                break
        self.assertTrue(result)

        name = "Mother Teresa"
        birthdate = "August 26, 1910"
        for x in authors:
            if x["name"] == name:
                self.assertEqual(x["birthdate"], birthdate)
                self.assertIsNotNone(x["bio"])
                result = True
                break
        self.assertTrue(result)

        name = "Dr.Seuss"
        birthdate = "March 02, 1904"
        for x in authors:
            if x["name"] == name:
                self.assertEqual(x["birthdate"], birthdate)
                self.assertIsNotNone(x["bio"])
                result = True
                break
        self.assertTrue(result)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AuthorSpiderTest)
    unittest.TextTestRunner().run(suite)
