import unittest
import os
from flask_injector import singleton
from injector import Injector
from scraper.model.entities import Database
from scraper.services import SERVICES
from scraper.services.quote_service import QuoteService


class QuoteServiceTest(unittest.TestCase):
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

        self.injector = Injector(modules=[configure])
        self.db = self.injector.get(Database)

    def tearDown(self):
        self.db.model.drop_all_tables(with_all_data=True)

    def TestQuoteServices(self):
        quote_service: QuoteService = self.injector.get(QuoteService)

        self.assertTrue(True)
        self.assertIsNotNone(quote_service)

        # Testing if database is empty #
        quotes = quote_service.list()
        self.assertFalse(quotes)

        # Testing DB insertion #
        text = "text1"
        author = "author1"
        result = quote_service.create_quote(text=text, author=author)
        self.assertIsNotNone(result)

        text = "text2"
        author = "author2"
        result = quote_service.create_quote(text=text, author=author)
        self.assertIsNotNone(result)

        text = "text3"
        author = "author1"
        result = quote_service.create_quote(text=text, author=author)
        self.assertIsNotNone(result)

        # Testing DB insertion of entry with duplicate "text" field #
        text = "text3"
        author = "author1"
        result = quote_service.create_quote(text=text, author=author)
        self.assertIsNone(result)

        # Testing listing of elements in DB #
        quotes = quote_service.list()
        self.assertIsNotNone(quotes)
        self.assertTrue(len(quotes) == 3)

        for x in quotes:
            if x["text"] == "text1":
                self.assertEqual(x["author"], "author1")
                result = True
                break
        self.assertTrue(result)

        for x in quotes:
            if x["text"] == "text2":
                self.assertEqual(x["author"], "author2")
                result = True
                break
        self.assertTrue(result)

        for x in quotes:
            if x["text"] == "text3":
                self.assertEqual(x["author"], "author1")
                result = True
                break
        self.assertTrue(result)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(QuoteServiceTest)
    unittest.TextTestRunner().run(suite)
