
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from weibo.spiders.topspider import TopspiderSpider
from weibo.spiders.weibospider import WeibospiderSpider
import logging
from scrapy.utils.project import get_project_settings


configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks

def crawl():

    yield runner.crawl(TopspiderSpider)
    logging.info("TopspiderSpider is stopped")
    yield runner.crawl(WeibospiderSpider)
    reactor.stop()

while True:
    logging.info("new cycle is starting")
    crawl()
    reactor.run() # the script will block here until the last crawl call is finished