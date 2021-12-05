# # Define here the models for your scraped items
# #
# # See documentation in:
# # https://docs.scrapy.org/en/latest/topics/items.html

# from scrapy_djangoitem import DjangoItem
# import sys
# sys.path.append("..")  # Adds higher directory to python modules path.
# from products.models import Product


# class ProductscraperItem(DjangoItem):
#     django_model = Product

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ProductItem(Item):
    barcode = Field()
    name = Field()
    company_name = Field()
    ingredients = Field()
    size = Field()
    categories = Field()
    image_link = Field()
    time_created = Field()
