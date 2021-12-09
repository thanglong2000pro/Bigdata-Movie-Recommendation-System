import scrapy
from imdb_crawler.items import MovieItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lorem_text import lorem # nho xoa thang nay khi xong viec

SEARCH_QUERY = (
    'https://www.imdb.com/search/title?'
    'title_type=feature&'
    'user_rating=1.0,10.0&'
    'count=250'
)

class MovieSpider(CrawlSpider):
    name = 'movie'
    allowed_domains = ['imdb.com']
    start_urls = [SEARCH_QUERY]
    index = 0

    rules = (Rule(
        LinkExtractor(restrict_css=('div.desc a')),
        follow=True,
        callback='parse_query_page',
    ),)

    def parse_query_page(self, response):
        data = MovieItem()
        items = response.xpath('//div[@class="lister-item mode-advanced"]')
        for item in items:
            item = item.xpath('.//div[@class="lister-item-content"]')

            self.index = self.index + 1
            data['id'] = self.index
            
            url = item.xpath('.//h3[@class="lister-item-header"]/a/@href').get(default="").strip()
            data['imdb_url'] = response.urljoin(response.request.url[0:20]) + url

            data['title'] = item.xpath('.//h3[@class="lister-item-header"]/a/text()').get(default='').strip()
            
            years = item.xpath('.//h3[@class="lister-item-header"]/span[@class="lister-item-year text-muted unbold"]/text()').get(default='()').strip()
            data['year'] = years[years.find("(")+1:years.find(")")]
            if not data['year'].isdigit():
                data['year'] = ''
            # years = [int(word) for word in years.split() if word.isdigit()]
            # if not years:
            #     years = ''
            # else:
            #     years = years[0]
            # data['year'] = years
            
            data['certificate'] = item.xpath('.//span[@class="certificate"]/text()').get(default='').strip()
            
            runtime = item.xpath('.//span[@class="runtime"]/text()').get(default='').strip()
            data['runtime'] = runtime.split(' ')[0].replace(",", "")
            
            genres = item.xpath('.//span[@class="genre"]/text()').get(default='').strip().split(',')
            data['genre'] = [genre.strip() for genre in genres]
            
            data['rating'] = item.xpath('.//div[@class="inline-block ratings-imdb-rating"]/strong/text()').get(default='').strip()
            data['metascore'] = item.xpath('.//div[@class="inline-block ratings-metascore"]/span/text()').get(default='').strip()
            
            # fake description cho dl no lon
            # num_p = 3
            # description = item.xpath('.//p[@class="text-muted"]/text()').get(default='').strip()
            description = lorem.paragraph()
            for i in range(4):
                description += " " + lorem.paragraph()
            # description = lorem.sentence()
            data['description'] = description #+ lorem.words(words) #+ lorem.paragraphs(num_p)
            
            director = item.xpath('.//p[@class]/a/text()').get(default='').strip()
            
            stars = item.xpath('.//p[@class]/a/text()').getall()
            data['star'] = []
            for star in stars:
                if star.strip() != director:
                    data['star'].append(star.strip())
            
            if director != 'See full summary' and director != "Add a Plot" and director != "See full synopsis":
                data['director'] = director
            else:
                data['director'] = ''
            
            data['vote'] = item.xpath('.//p[@class="sort-num_votes-visible"]/span[@name="nv"]/text()').get(default='').strip().replace(',', '')
            
            yield data
        
        # NOTE: it only crawl 3 pages because 2 GET is the same (duplicated) but i don't know why
        # next_page = response.css('div.desc a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)