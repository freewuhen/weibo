# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from scrapy.exceptions import DropItem
import json
import re
from weibo.Tool.OperationaDB import Operational_DB
class TopPipeline(object):

    def __init__(self):
        #self.file = open('resource/Top.txt', 'wb')
        self.file = open('Top.txt','at',encoding='utf-8')

    def process_item(self, item, spider):

        if item.item_name is 'TopItem':
            line = (json.dumps(dict(item),ensure_ascii=False) + "\n")
            self.file.write(line)

            logging.info("TopPipeline is running ")

        return item
class WeiboPipeline(object):
    def __init__(self):
        # self.file = open('weibo/resource/HotWeibo.txt', 'wb')
        self.database = Operational_DB()
    def process_item(self, item, spider):
        if item.item_name is 'WeiboItem' and item['flag'] is True and item['comments_count'] > 100:
            weibo_id = item['id']
            hottop = item['hottop']
            #数据库中没有相同的微博
            if self.database.check_weibo(weibo_id) is True:
                self.database.insert_weibo(weibo_id,hottop)

            logging.info("WeiboPipeline is running ")
        return item

class CommentPipeline(object):
    def __init__(self):

        self.file = open('commenttest.txt', 'at',encoding='utf-8')
        #匹配中文的正则表达式
        self.pattern = re.compile(r"[\u4e00-\u9fa5，。！？?! ]{1,}")
    def remove_text_dirty(self,oldstr):
            logging.info("oldstr:" + oldstr)
            oldstr = oldstr.replace("\n", "")#去掉评论所有的换行符
            count = oldstr.count("<a")#统计评论中<a>标签的数量

            for i in range(0,count): # 对评论中<a>标签逐一进行处理
                if oldstr.count("<a") is 0: #如果评论中没有<a>标签
                    break
                font = oldstr.index("<a")
                tail = oldstr.index("</a>")
                dirty = oldstr[font:tail+4] #获取到评论中当前<a>标签的内容
                oldstr = oldstr.replace(dirty,"") #去除评论中当前<a>标签的内容
            logging.info("newstr:"+oldstr)
            match = self.pattern.match(oldstr)
            logging.info("match:"+str(match))
            if match:
                #返回匹配到的中文内容
                return match.group()
            else:
                #没有中文返回汉字
                return None
    def make_time(self,time):
        logging.info("oldtime:"+time)
        time = time.replace(" +0800 2018", "")[8:]
        t = "2018-08-"
        return t + time

    def process_item(self, item, spider):
        if item.item_name is 'CommentItem':
            item['text'] = self.remove_text_dirty(item['text'])
            if item['flag'] is True and item['text'] is not None:
                item['time'] = self.make_time(item['time'])
                line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                self.file.write(line)
            else:
                logging.info("this item is invalid")
            logging.info("CommentPipeline is running ")
        return item
class ProxyPopeline(object):
    def __init__(self):
        # self.file = open('weibo/resource/proxy.txt', 'wb')
        self.database = Operational_DB()
    def process_item(self, item, spider):

        if item.item_name is 'ProxyItem':
            # line = (json.dumps(dict(item)) + "\n").encode()
            # self.file.write(line)
            ip = item['ip']
            port = item['port']
            ip_type = item['ip_type']
            self.database.insert_proxytable(ip,port,ip_type)
            logging.info("ProxyPopeline is running ")
        return item

