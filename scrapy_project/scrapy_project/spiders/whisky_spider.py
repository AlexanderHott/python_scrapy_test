from os.path import abspath

import scrapy
import scrapy.http
from parsel.selector import SelectorList


class WhiskySpider(scrapy.Spider):
    """Scraper that scrapes https://www.whiskyshop.com/scotch-whisky/all"""

    name: str = "whisky"
    start_urls: list[str] = ["https://www.whiskyshop.com/scotch-whisky/all"]

    def parse(self, response: scrapy.http.TextResponse):
        # products: SelectorList
        for products in response.css("div.product-item-info"):
            try:
                yield {
                    "name": products.css("a.product-item-link::text").get(),
                    "price": products.css("span.price::text").get().replace("£", ""),
                    "link": products.css("a.product-item-link").attrib["href"],
                }
            except:
                yield {
                    "name": products.css("a.product-item-link::text").get(),
                    "price": "sold out",
                    "link": products.css("a.product-item-link::attrib(href)").attrib["href"],
                }
