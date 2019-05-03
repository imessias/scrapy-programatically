# Scrapy Web Crawler with Pony ORM Database service
Web Crawler test using the [Scrapy](https://scrapy.org/) application framework.

See Scrapy documentation [here](https://docs.scrapy.org/en/latest/index.html).

## Requirements
- Python3, install [here](https://www.python.org/downloads/)
- Virtual environments

## Setup
Install requirements
```
virtualenv --python=python3 .venv
source .venv/bin/activate
pip install -r requirements-linux.txt
```
Install using windows cmd
 - **Troubleshooting** - see the following [post](https://github.com/benfred/implicit/issues/76#issuecomment-468733978) in case of installation errors
```
virtualenv --python=python3 .venv
".venv/Scripts/activate"
pip install -r requirements.txt
```

## Run
Make sure you are in the virtual environment and run
```
python app.py
```

### Database
The scraped data is stored in a SQLite database using [Pony ORM](https://ponyorm.org/).


## Change log
- **26/04/2019** - Started project following the Scrapy tutorial [here](https://docs.scrapy.org/en/latest/intro/tutorial.html). Built the database services. Temporary fix on the issue of injecting objects into the spiders.
- **29/04/2019** - Fixed import issues in project. Trying to solve issues in the generation of the database tables.
- **03/05/2019** - Fixed issue in generating tables.