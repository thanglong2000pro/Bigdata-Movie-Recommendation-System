# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id              = scrapy.Field() # integer      (ex: 1)
    imdb_url        = scrapy.Field() # string       (ex: "https://")
    title           = scrapy.Field() # string
    rating          = scrapy.Field() # float 
    year            = scrapy.Field() # integer
    vote            = scrapy.Field() # integer
    metascore       = scrapy.Field() # integer
    star            = scrapy.Field() # array        (ex: ["Ron Wesley", "Harry Potter", "Hermione"])
    certificate     = scrapy.Field() # string
    description     = scrapy.Field() # string
    director        = scrapy.Field() # string
    runtime         = scrapy.Field() # integer
    genre           = scrapy.Field() # array        (ex: ["war", "sport"])
    pass
