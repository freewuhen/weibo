# -*- coding: utf-8 -*-
import scrapy
import json
import time
from weibo.items import  TopItem
from weibo.items import  WeiboItem
import logging
class TopspiderSpider(scrapy.Spider):
    name = "topspider"
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

            link = card.get('scheme').replace("p/searchall","api/container/getIndex")+"&page_type=searchall"
            yield scrapy.Request(link,meta={'hottop':card.get('desc')},callback=self.weibo_parse)

    def weibo_parse(self,response):
        weibo_item = WeiboItem()
        # id = scrapy.Field()
        # text = scrapy.Field()
        # user = scrapy.Field()
        # link = scrapy.Field()

        result = json.loads(response.text)

        correct_flog_list = [11,7]
        try:
            for i in range(0,2):
                gourp = result.get('data').get('cards')[i]
                group_flag = gourp.get('card_type')

                if(group_flag in correct_flog_list ):
                    card_group = gourp.get('card_group')
                    if card_group is None:
                        break
                    else:
                        for weibo in card_group:
                            self.all_counter = self.all_counter+1
                            if weibo.get('card_type') is 9:
                                comments_count = weibo.get('mblog').get('comments_count')

                                weibo_item['flag'] = True
                                weibo_item['hottop'] = response.meta['hottop']
                                weibo_item['id'] = weibo.get('mblog').get('id')
                                weibo_item['comments_count'] = comments_count
                                yield weibo_item
                            else:
                                weibo_item['flag'] = False
                                self.dirty_two_counter = self.dirty_two_counter+1
                                logging.info("dirty 2")
                                yield weibo_item
                else:
                    weibo_item['flag'] = False
                    self.dirty_one_counter = self.dirty_one_counter+1
                    logging.info("dirty 1")
                    yield weibo_item
        except IndexError:
            self.error_counter = self.error_counter+1
            weibo_item['flag'] = False
            logging.info("IndexError")
            yield weibo_item
    def close(spider, reason):
        logging.info("closed is running ")
        all_amount = spider.all_counter
        dirty_one_rate = "dirty_one_rate:"+str(spider.dirty_one_counter/all_amount*100)+"%\n"
        dirty_two_rate = "dirty_two_rate:"+str(spider.dirty_two_counter/all_amount*100)+"%\n"
        erorr_rate = "erorr_rate:"+str(spider.error_counter/all_amount*100)+"%\n"
        logging.info(dirty_one_rate)
        logging.info(dirty_two_rate)
        logging.info(erorr_rate)
        # from scrapy import cmdline
        # cmdline.execute('scrapy crawl weibospider'.split())








