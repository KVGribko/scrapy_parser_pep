import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        links = response.css(
            "section[id=numerical-index] tr td:nth-child(2) a::attr(href)"
        ).getall()

        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = response.css("h1.page-title::text").get().split(" – ")
        status = response.css("dt:contains('Status') + dd abbr::text").get()
        data = {
            "number": number,
            "name": name,
            "status": status,
        }
        yield PepParseItem(data)
