# -*- coding: utf-8 -*-
import scrapy
import json
import time
from weibo.items import  TopItem

import logging
class NewtopspiderSpider(scrapy.Spider):
    name = "newtopspider"
    allowed_domains = ["m.weibo.cn"]
    start_urls = [
        "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type=realtimehot&mi_cid=100103&pos=0_0&c_type=30&display_time=1532775306&luicode=10000011&lfid=231583", ]
    custom_settings = {
        "USER_AGENT": "User-Agent: MQQBrowser/26 Mozilla/5.0 (linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    }
    cookie = {
        'Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2':'1533036122',
        'Hm_lvt_3406180e5d656c4789c6c08b08bf68c2':'1533036122',
        'JSESSIONID':'6203647B2AF9A21DA805EFAEDD0C583C',
    }
    all_counter = 0
    dirty_one_counter = 0
    dirty_two_counter = 0
    error_counter = 0

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],cookies=self.cookie,callback=self.parse)
    def parse(self, response):
        result = json.loads(response.text)

        card_group = result.get('data').get('cards')[0].get('card_group')
        for i in range(1,len(card_group)-1):
            card = card_group[i]
            item = TopItem()
                # rank = scrapy.Field()
                # hot = scrapy.Field()
                # title = scrapy.Field()
                # link = scrapy.Field()
            item['time'] = time.time()
            item['rank'] = i
            item['hot'] = int(card.get('desc_extr'))
            item['title'] = card.get('desc')
            yield item;

