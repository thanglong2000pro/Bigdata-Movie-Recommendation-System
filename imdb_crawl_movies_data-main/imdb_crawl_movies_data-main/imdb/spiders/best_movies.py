import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1[@data-testid='hero-title-block__title']/text()").get(),
            'year': response.xpath("(//li[@class='ipc-inline-list__item']/a)[1]/text()").get(),
            'duration': response.xpath("//li[@class='ipc-inline-list__item']/text()").get(),
            'genres': response.xpath("(//div[@data-testid='genres']/a)[1]/text()").get(),
            'rating': response.xpath("(//div[@data-testid='hero-rating-bar__aggregate-rating__score'])[1]/span/text()").get(),
            'url': response.url,
        }