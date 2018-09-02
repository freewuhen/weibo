# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
from weibo.items import CommentItem
import json
import re
from weibo.Tool.OperationaDB import Operational_DB
import logging

class NewweibospiderSpider(scrapy.Spider):
    name = "newweibospider"
    allowed_domains = ["m.weibo.cn"]
    start_urls = 'https://m.weibo.cn/comments/hotflow?id={wid}&mid={mid}&max_id_type=0'
    # start_id = ['4268345371514938','4268497154934071','4268516783489064']
    start_id_index = 0;
    custom_settings = {
        "USER_AGENT": "User-Agent: MQQBrowser/26 Mozilla/5.0 (linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    }
    cookie = {
        '_T_WM': '35f482a7287c068583d5c250f541d3f3',
        'M_WEIBOCN_PARAMS': 'oid=4268225069366960&luicode=10000011&lfid=100103type%3D1%26q%3D%23%E5%85%A8%E7%8F%AD%E5%8F%AA%E6%9C%89%E5%84%BF%E5%AD%90%E6%B2%A1%E5%87%BA%E8%BF%87%E5%9B%BD%23%26t%3D10&uicode=20000061&fid=4268225069366960',
        'MLOGIN': 1,
        'SCF': 'AqZbTTvCA9H7LvNWZlAQfxziuvwZOeN2bwM4LaMtYcPXBDDBrx9_R0osncYZ4Z4jxUqjv5gYXbKY4rW31cBrPVQ',
        'SSOLoginState': '1533124011',
        'SUB': '_2A252Ze37DeThGeNN4lAU8y_MzDWIHXVVqfOzrDV6PUJbkdAKLRWlkW1NSZLmMhtNAzLRyulkeO0jlycwnTkT5bkK',
        'SUHB': '0jBYmDvwOHB2Qu',
        'WEIBOCN_FROM': '1110006030'
    }
    current_user_region = ''
    homepage_id_url_template = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode={luicode}&type=uid&value={value}&containerid={containerid}'
    homepage_url_template = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode={luicode}&type=uid&value={value}&containerid={containerid}'
    user_luicode = '20000174'
    current_url = ''
    counter = 0;
    all_counter = 0
    none_counter = 0
    fish_index = 0
    # emoji的正则表达式
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    # 过滤<span的正则表达式
    pattern = re.compile(r"[\u4e00-\u9fa5，。！？?!]{1,}")

    def __init__(self):
        logging.info("weibospider is running now")
        self.database = Operational_DB()
        # self.start_list = self.database.load_weibo()
        self.start_list = [('4270685695777606', 'test1',-1),('4270690414847430','test2',-1)]
        self.start_list = [list(e) for e in self.start_list]
    # 起始爬取链接处理
    def start_requests(self):

        self.current_url = self.start_urls.format(wid=self.start_list[self.start_id_index][0],
                                                  mid=self.start_list[self.start_id_index][0])
        #self.start_id_index = self.start_id_index + 1;
        yield Request(self.current_url, cookies=self.cookie, callback=self.parse)

    # 获取评论的内容
    def parse(self, response):
        max_id = 0
        try:
            weibo_id = self.start_list[self.start_id_index][0]
            hottop = self.start_list[self.start_id_index][1]
            # 将爬取的微博进行标记
            self.database.mark_weibo(weibo_id)
            # 处理过微博的计数器
            self.counter = self.counter + 1
            logging.info("counter:" + str(self.counter))

            # 获取当前抓取结果的json
            result = json.loads(response.text)

            commit_group = result.get('data').get('data')  # 获取当前抓取内容的评论组
            # 获取当前抓取内容的max_id,需要根据max_id生成下一页评论的获取链接
            max_id = result.get('data').get('max_id')

            # 对当前抓取内容的评论组的评论逐一进行处理
            for commit in commit_group:
                self.all_counter = self.all_counter + 1
                # time,user_id,text,region,like
                item = CommentItem()
                item['weibo_id'] = weibo_id
                item['hottop'] = hottop

                item['time'] = commit.get('created_at')
                text = commit.get('text')
                item['text'] = text
                item['user_id'] = commit.get('user').get('id')
                item['like'] = commit.get('like_count')

                logging.info("homepage_id_url is starting")
                uid = item['user_id']
                containerid = '100505'
                containerid = containerid + str(uid)
                # 生成获取主页id的请求链接
                logging.info("uid:" + str(uid))
                logging.info("containerid:" + str(containerid))
                logging.info("homepage_id_url is ready")
                homepage_id_url = self.homepage_id_url_template.format(uid=uid, luicode=self.user_luicode, value=uid,
                                                                       containerid=containerid)
                # 发送请求
                logging.info("Request next commit group")
                yield Request(homepage_id_url, meta={'uid': uid, 'item': item}, callback=self.homepage_id_parse)

            if max_id is not 0:  # 当前所有评论未抓取完成
                # 根据max_id生成下一页评论的获取链接
                nextPage_url = self.current_url + '&max_id=' + str(max_id)
                # 发送新的请求
                logging.info("Request next comment group")
                yield Request(nextPage_url, cookies=self.cookie, callback=self.parse)
            else:  # max_id == 0 ， 当前所有评论未抓取完成
                # 获取下一条微博
                logging.info("maxid is 0")
                next_weibo_url = self.get_nextweibo()
                if next_weibo_url is None:  # 所有微博爬取完毕
                    logging.info("this job is finished")
                    return

                yield Request(next_weibo_url, cookies=self.cookie, dont_filter=True, callback=self.parse)
                # self.get_nextweibo()
        except AttributeError:  # 处理单条微博爬取极限问题
                self.start_list[self.start_id_index][2] = max_id
                # 获取下条微博id
                logging.info("This spider has been overloaded")
                next_weibo_url = self.get_nextweibo()
                if next_weibo_url is None:  # 所有微博爬取完毕
                    logging.info("this job is finished")
                    return
                logging.info("Request next weibo")
                yield Request(next_weibo_url, cookies=self.cookie, callback=self.parse)

    # 获取下一条微博请求链接
    def get_nextweibo(self):
        self.start_id_index = self.start_id_index + 1
        logging.info("get_nextweibo is running")
        if self.start_id_index > len(self.start_list) - 1:  # 所有的微博评论爬取完毕
            logging.info("self.start_id_index > len(self.start_list)-1")
            next = self.find_Netoffish()
            if next is -1:
                logging.info("complete finished ")
                return None
            else:
                logging.info("new cycle")
                self.start_id_index = self.fish_index

        return self.gen_nextweibo_url()

    # 生成下一条微博请求链接
    def gen_nextweibo_url(self):

        logging.info(self.start_id_index)
        next_weibo_id = self.start_list[self.start_id_index][0]
        max_id = self.start_list[self.start_id_index][2]
        # start_list的游标加一

        # 生成下一条微博的爬取链接
        next_weibo_url = self.start_urls.format(wid=next_weibo_id, mid=next_weibo_id)

        #当前链接记忆器
        self.current_url = next_weibo_url

        if max_id is not -1: #如果该条微博 处理过且没有处理完
            #延续之前的请求继续爬取
            next_weibo_url = self.current_url + '&max_id=' + str(max_id)


        # 发送请求

        return next_weibo_url
    # 根据用户的id获取用户所在的地区
    def get_user_region(self, uid):
        logging.info("get_user_region is running ")
        containerid = '100505'
        containerid = containerid + uid
        # 生成获取主页id的请求链接
        homepage_id_url = self.homepage_id_url_template.format(uid=uid, luicode=self.user_luicode, value=uid,
                                                               containerid=containerid)
        # 发送请求
        yield Request(homepage_id_url, meta={'uid': uid}, callback=self.homepage_id_parse)

    # 处理获取主页id的请求
    def homepage_id_parse(self, response):
        item = response.meta['item']
        try:
            logging.info("homepage_id_parse is running ")
            uid = response.meta['uid']
            result = json.loads(response.text)
            # 获取主页的id
            homepage_id = result.get('data').get('tabsInfo').get('tabs')[0].get('containerid')
            logging.info(homepage_id)
            # 生成主页的请求链接
            homepage_url = self.homepage_url_template.format(uid=uid, luicode=self.user_luicode, value=uid,
                                                             containerid=homepage_id)

            yield Request(homepage_url, meta={'item': item}, callback=self.region_parse)
        except AttributeError:
            # 获取的信息无效效
            item['flag'] = False
            yield item

    def region_parse(self, response):
        item = response.meta['item']
        try:
            logging.info("region_parse is running")
            result = json.loads(response.text)
            region = result.get('data').get('cards')[0].get('card_group')[0].get('item_content')
            logging.info(region)
            item['region'] = region
            # 获取的信息有效
            item['flag'] = True
            yield item

        except IndexError:
            logging.error("IndexError")
            item['flag'] = False
            yield item

    def find_Netoffish(self):
        for i in range(self.fish_index,len(self.start_list)):
            if self.start_list[i][2] is not -1:
                self.fish_index = i
                return i
        return -1;

    def close(spider, reason):
        logging.info("stop")

