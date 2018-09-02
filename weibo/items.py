# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    item_name = 'WeiboItem'

    flag = scrapy.Field()
    id = scrapy.Field()
    hottop = scrapy.Field()
    comments_count = scrapy.Field()

class TopItem(scrapy.Item):
    item_name = 'TopItem'

    flag = scrapy.Field()
    time = scrapy.Field()
    rank = scrapy.Field()
    hot = scrapy.Field()
    title = scrapy.Field()
    #link = scrapy.Field()
class CommentItem(scrapy.Item):
    item_name = 'CommentItem'

    flag = scrapy.Field()
    weibo_id = scrapy.Field()
    hottop = scrapy.Field()
    time = scrapy.Field()
    user_id= scrapy.Field()
    text = scrapy.Field()
    like = scrapy.Field()
    region = scrapy.Field()
class UserItem(scrapy.Item):
    item_name ='UserItem'
    id = scrapy.Field()
    region = scrapy.Field()
class ProxyItem(scrapy.Item):
    item_name ='ProxyItem'
    ip = scrapy.Field()
    port = scrapy.Field()
    ip_type = scrapy.Field()


