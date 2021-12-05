# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from scrapy.exceptions import DropItem
from productscraper.productscraper.models import Product, db_connect, create_table


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        item.setdefault('name', '')
        item.setdefault('company_name', '')
        item.setdefault('ingredients', '')
        item.setdefault('size', '')
        item.setdefault('categories', '')
        item.setdefault('image_link', '')
        item.setdefault('time_created', func.now())
        return item


class SaveProductsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save products in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        product = Product()
        product.barcode = item["barcode"]
        product.name = item["name"]
        product.company_name = item["company_name"]
        product.ingredients = item["ingredients"]
        product.size = item["size"]
        product.categories = item["categories"]
        product.image_link = item["image_link"]
        product.time_created = item["time_created"]

        # check whether the product exists
        exist_product = session.query(
            Product).filter_by(name=product.barcode).first()
        if exist_product is not None:  # the current product exists
            product.product = exist_product
        else:
            product.product = product

        try:
            session.add(product)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
