import unittest
import os
#from os import path
from flask_injector import singleton
from injector import Injector
from scraper.model.entities import Database
from scraper.services import SERVICES
from scraper.services.author_service import AuthorService


class AuthorServiceTest(unittest.TestCase):
    #DATABASE_URL = path.join("..", "..", "data", "database-test.db")

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

    def testAuthorServices(self):
        author_service: AuthorService = self.injector.get(AuthorService)

        self.assertTrue(True)
        self.assertIsNotNone(author_service)

        # Testing if database is empty #
        authors = author_service.list()
        self.assertFalse(authors)

        # Testing DB insertion #
        name = "Albert Einstein"
        birthdate = "sometime"
        bio = "something"
        result = author_service.create_author(name, birthdate, bio)
        self.assertIsNotNone(result)

        name = "Stephen Hawking"
        birthdate = "sometime"
        bio = "something"
        result = author_service.create_author(name=name, birthdate=birthdate, bio=bio)
        self.assertIsNotNone(result)

        # Testing DB insertion of duplicate primary key #
        name = "Albert Einstein"
        result = author_service.create_author(name=name)
        self.assertIsNone(result)

        # Testing listing of elements in DB #
        authors = author_service.list()
        self.assertIsNotNone(authors)
        self.assertCountEqual(len(authors), 2)

        for x in authors:
            if x["name"] == "Albert Einstein":
                self.assertIsNone(x["birthdate"])
                self.assertIsNone(x["bio"])
                result = True
                break
        self.assertTrue(result)

        for x in authors:
            if x["name"] == "Stephen Hawking":
                self.assertEqual(x["birthdate"], birthdate)
                self.assertEqual(x["bio"], bio)
                result = True
                break
        self.assertTrue(result)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AuthorServiceTest)
    unittest.TextTestRunner().run(suite)
