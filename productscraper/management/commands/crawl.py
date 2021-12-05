from django.core.management.base import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from productscraper.productscraper.spiders.products_spider import ProductsSpider
from productscraper.productscraper import settings as my_settings
from multiprocessing import Process, Queue


def f(q, barcode, *args, **options):
    try:
        configure_logging()
        settings = Settings()
        settings.setmodule(my_settings)

        runner = CrawlerRunner(settings=settings)
        spider = ProductsSpider
        d = runner.crawl(spider, barcode=barcode)
        d.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)
        q.put(None)
    except Exception as e:
        q.put(e)


def handle_scrape(barcode):
    q = Queue()
    p = Process(target=f, args=(q, barcode))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


# class CrawlProduct(BaseCommand):
#     help = 'Release spider'

#     def handle(self, barcode, *args, **options):
#         configure_logging()
#         settings = Settings()
#         settings.setmodule(my_settings)

#         runner = CrawlerRunner(settings=settings)
#         spider = ProductsSpider
#         d = runner.crawl(spider, barcode=barcode)
#         d.addBoth(lambda _: reactor.stop())
#         reactor.run(installSignalHandlers=False)
