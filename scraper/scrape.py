import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.spiders.quotes_spider import QuotesSpider
from scraper.spiders.author_spider import AuthorSpider
from scraper.spiders import SPIDERS
from scraper.services.author_service import AuthorService
from injector import inject

class Scraper:
    @inject
    def __init__(self, spider: AuthorSpider, service: AuthorService):
        self.spider = spider
        self.service = service
        self.run_spiders()

    def run_spiders(self):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'SERVICE': self.service,
            'LOG_LEVEL': 'INFO'
        })

        #for spider in SPIDERS: 
         #   process.crawl(spider)
        process.crawl(AuthorSpider)
        process.start()
