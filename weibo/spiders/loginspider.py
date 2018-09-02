# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.http.cookies import CookieJar
# from scrapy import log
# class LoginspiderSpider(scrapy.Spider):
#     name = "loginspider"
#     allowed_domains = ["m.weibo.cn"]
#     start_urls = 'https://passport.weibo.cn/sso/login'
#     custom_settings = {
#         "USER_AGENT": "User-Agent: MQQBrowser/26 Mozilla/5.0 (linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
#     }
#     login_data = {
#         'client_id':'',
#         'code':'',
#         'ec':'0',
#         'entry':'mweibo',
#         'hff':'',
#         'hfp':'',
#         'loginfrom':'',
#         'mainpageflag':'1',
#         'pagerefer':"https://m.weibo.cn/",
#         'password':'wwt123456789lp',
#         'qq':'',
#         'r':"https://m.weibo.cn /",
#         'savestate':'1',
#         'username':'17865682502@163.com',
#         'wentry':''
#
#     }
#     def start_requests(self):
#         cookie_jar = CookieJar()
#         return [scrapy.FormRequest(url=self.start_urls,formdata=self.login_data,meta={'dont_merge_cookies': True,'cookiejar': cookie_jar},callback=self.parse)]
#     def parse(self, response):
#
#         print(response.meta['cookiejar'])
