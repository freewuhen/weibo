# -*- coding: utf-8 -*-
import scrapy
import json
import logging
class UserspiderSpider(scrapy.Spider):
    name = "userspider"
    allowed_domains = ["m.weibo.cn"]
    luicode = '20000174'
    containerid = '100505'
    uid = '5502161828'
    start_urls = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode={luicode}&type=uid&value={value}&containerid={containerid}'
    custom_settings = {
        "USER_AGENT": "User-Agent: MQQBrowser/26 Mozilla/5.0 (linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    }
    def start_requests(self):
        containerid = self.containerid+self.uid
        homepage_id_url = self.start_urls.format(uid=self.uid,luicode=self.luicode,value=self.uid,containerid=containerid)
        yield scrapy.Request(homepage_id_url,callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        homepage_id = result.get('data').get('tabsInfo').get('tabs')[0].get('containerid')
        logging.info(homepage_id)
        homepage_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode={luicode}&type=uid&value={value}&containerid={containerid}'
        homepage_url = homepage_url.format(uid=self.uid,luicode=self.luicode,value=self.uid,containerid=homepage_id)
        yield scrapy.Request(homepage_url,callback=self.region_parse)
    def region_parse(self, response):
        result = json.loads(response.text)
        region = result.get('data').get('cards')[0].get('card_group')[0].get('item_content')
        logging.info(region)

