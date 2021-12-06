from pathlib import Path
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

BOT_NAME = 'productscraper'

SPIDER_MODULES = ['productscraper.productscraper.spiders']
NEWSPIDER_MODULE = 'productscraper.productscraper.spiders'

# Database Connection String

# PostgresQL
CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}".format(
    drivername="postgresql",
    user=env('DB_USER'),
    passwd=env('DB_PASSWORD'),
    host=env('DB_HOST'),
    port=env('DB_PORT'),
    db_name=env('DB_NAME'),
)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'productscraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'productscraper.productscraper.pipelines.DefaultValuesPipeline': 100,
    'productscraper.productscraper.pipelines.SaveProductsPipeline': 200,
}
