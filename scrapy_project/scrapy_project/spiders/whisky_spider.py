import scrapy
import scrapy.http
from parsel.selector import SelectorList
import collections.abc as collections_abc


class WhiskySpider(scrapy.Spider):
    """Scraper that scrapes https://www.whiskyshop.com/scotch-whisky/all"""

    name: str = __name__.split(".")[-1]
    start_urls: list[str] = ["https://www.whiskyshop.com/scotch-whisky/all"]

    # https://docs.python.org/3/library/typing.html#typing.Generator
    def parse(
        self, response: scrapy.http.TextResponse
    ) -> collections_abc.Generator[dict[str, str], None, None]:
        """Parse the response and yield the whisky name, price, and link."""

        products: SelectorList
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
                    "link": products.css("a.product-item-link::attrib(href)").attrib[
                        "href"
                    ],
                }

        next_page = response.css("a.action.next").attrib["href"]

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
