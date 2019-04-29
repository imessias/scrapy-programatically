from flask_injector import inject
from scraper.services.quote_service import QuoteService


class QuoteDatabasePipeline(object):
    @inject
    def __init__(self, quote_service: QuoteService):
        self.quote_service = quote_service

    def process_item(self, item, spider):
        self.quote_service.create_quote(item["text"], item["author"])
        return item