import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from flask_injector import inject
from scraper.services.author_service import AuthorService
from scraper.item_pipelines.author_pipeline import AuthorDatabasePipeline


class AuthorSpider(scrapy.Spider):
    name = "author"
    custom_settings = {
        "ITEM_PIPELINES": {"item_pipelines.author_pipeline.AuthorDatabasePipeline": 1}
    }
    start_urls = ["http://quotes.toscrape.com/"]

    def __init__(self):
        scrapy.Spider.__init__(self)

    def parse(self, response):
        #follow links to author pages
        for href in response.css(".author + a::attr(href)"):
            yield response.follow(href, self.parse_author)

        #follow pagination links
        for href in response.css("li.next a::attr(href)"):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        select = response.xpath("//div[@class='author-details']")
        l = AuthorLoader(item=Author(), selector=select)
        l.add_xpath("name", "./h3[@class='author-title']/text()")
        l.add_xpath("birthdate", ".//span[@class='author-born-date']/text()")
        l.add_xpath("bio", "./div[@class='author-description']/text()")
        yield l.load_item()

def remove_newline(input):
    #return input.replace("\n", " ")
    return " ".join(input.split())

class Author(scrapy.Item):
    name = scrapy.Field()
    birthdate = scrapy.Field()
    bio = scrapy.Field()


class AuthorLoader(ItemLoader):
    default_input_processor = MapCompose(remove_newline)
    default_output_processor = TakeFirst()
