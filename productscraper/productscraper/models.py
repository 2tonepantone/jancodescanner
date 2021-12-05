from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Product(Base):
    __tablename__ = "products_product"

    id = Column(Integer, primary_key=True)
    barcode = Column('barcode', String(13), unique=True)
    name = Column('name', Text())
    company_name = Column('company_name', Text())
    ingredients = Column('ingredients', Text())
    size = Column('size', Text())
    categories = Column('categories', Text())
    image_link = Column('image_link', Text())
    time_created = Column('time_created', DateTime(timezone=True))
