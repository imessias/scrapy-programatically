from scraper.item_pipelines.author_pipeline import AuthorDatabasePipeline
from scraper.item_pipelines.quote_pipeline import QuoteDatabasePipeline

PIPELINES = [
    AuthorDatabasePipeline,
    QuoteDatabasePipeline
]