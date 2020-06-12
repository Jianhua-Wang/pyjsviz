import scrapy
import re

class NWinnerItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()


class NWinnerSpider(scrapy.Spider):
    """Scrapes the country and link text of the Nobel-winners"""

    name = 'nwinners_list'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
    ]

    def parse(self, response):
        h3s = response.xpath('//h3')

        for h3 in h3s:
            print(h3.extract())
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    text = w.xpath('descendant-or-self::text()').extract()
                    yield NWinnerItem(
                        country=country[0],
                        name=text[0],
                        link_text = ' '.join(text)
                    )