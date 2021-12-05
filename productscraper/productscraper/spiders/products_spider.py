from scrapy.crawler import CrawlerRunner
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
import scrapy

from productscraper.productscraper.items import ProductItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["jancode.xyz"]

    def start_requests(self):
        urls = [f'https://www.jancode.xyz/{self.barcode}/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        product_loader = ItemLoader(item=ProductItem(), response=response)
        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css(
            "barcode", '.table-block td span::text'
        )
        product_loader.add_css(
            "name", '.keni-section h2::text'
        )
        product_loader.add_xpath(
            "company_name", '//*[contains(text(),"会社名")]/parent::tr/td/a/text()'
        )
        product_loader.add_xpath(
            "ingredients", '//*[contains(text(),"原材料")]/parent::tr/td/text()'
        )
        product_loader.add_xpath(
            "size", '//*[contains(text(),"内容量")]/parent::tr/td/text()'
        )
        product_loader.add_xpath(
            "categories", '//*[contains(text(),"商品ジャンル")]/parent::tr/td/a/text()'
        )
        product_loader.add_xpath(
            "image_link", '//*[contains(text(),"商品イメージ")]/parent::tr/td/img/@src'
        )

        yield product_loader.load_item()
