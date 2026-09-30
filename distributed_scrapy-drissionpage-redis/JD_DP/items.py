# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class JdDpItem:
    # define the fields for your item here like:
    # name: str | None = None
    
    title: str | None = None
    price: str | None = None
    QuantitySold: str | None = None
    StoreName: str | None = None
