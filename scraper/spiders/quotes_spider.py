import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from flask_injector import inject


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        "ITEM_PIPELINES": {"item_pipelines.quote_pipeline.QuoteDatabasePipeline": 1}
    }
    allowed_domains = [
        "quotes.toscrape.com",
    ]
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]

    @inject
    def __init__(self):
        scrapy.Spider.__init__(self)

    def parse(self, response):
        for quote in response.xpath("//div[@class=\"quote\"]"):
            l = ItemLoader(item=Quote(), selector=quote)
            l.add_xpath("text", "./span[@class=\"text\"]/text()")
            l.add_xpath("author", ".//small[@class=\"author\"]/text()")
            #l.add_xpath("tags", ".//div[@class=\"tags\"]/a[@class=\"tag\"]/text()")
            yield l.load_item()

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class Quote(scrapy.Item):
    text = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    #tags = scrapy.Field()