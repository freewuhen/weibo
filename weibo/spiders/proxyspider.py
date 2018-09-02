# -*- coding: utf-8 -*-
import scrapy
from weibo.items import  ProxyItem

class ProxyspiderSpider(scrapy.Spider):
    name = "proxyspider"
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://www.xicidaili.com']
    custom_settings = {
        "USER_AGENT": "User-Agent: MQQBrowser/26 Mozilla/5.0 (linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    }

    # cookie = {
    #     'Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2':'1533038695',
    #     'Hm_lvt_3406180e5d656c4789c6c08b08bf68c2':'1533036122',
    #     'JSESSIONID':'6203647B2AF9A21DA805EFAEDD0C583C',
    # }
    # def start_requests(self):
    #     yield scrapy.Request(url=self.start_urls[0],cookies=self.cookie,callback=self.parse)
    def parse(self, response):
        item = ProxyItem()
        proxy_list = response.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/table/tbody')

        for proxy in proxy_list:
                proxy_ip = proxy.xpath('span[1]/li/text()').extract()
                proxy_port = proxy.xpath('span[2]/li/text()').extract()
                proxy_type = proxy.xpath('span[4]/li/a/text()').extract()

                item['ip'] = proxy_ip[0]
                item['port'] = proxy_port[0]
                item['ip_type'] = proxy_type[0]
                yield item

