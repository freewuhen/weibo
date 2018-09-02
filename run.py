from scrapy.crawler import CrawlerProcess
from weibo.spiders.newweibospider import NewweibospiderSpider
import logging
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(NewweibospiderSpider)
process.start()

logging.info("finished ")
