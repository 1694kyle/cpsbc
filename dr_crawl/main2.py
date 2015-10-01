from spiders.dr_spider import DrSpider

# scrapy api imports
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings


# crawler gen
def build_spider():
    form_data = get_form_data()
    yield DrSpider(kwargs=form_data.next())


def get_form_data():
    postal_codes = [code.strip() for code in open('postal_codes')]
    for postal_code in postal_codes:
        for radius in range(1,3):
            yield {'postal_code': postal_code, 'radius': radius}


TO_CRAWL = build_spider()

# crawlers that are running
RUNNING_CRAWLERS = []


def spider_closing(spider):
    """
    Activates on spider closed signal
    """
    print 'spider closed: {}'
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()

# set up the crawler and start to crawl one spider at a time
for spider in TO_CRAWL:
    settings = get_project_settings()

    crawler_obj = spider
    crawler = Crawler(crawler_obj, settings)

    RUNNING_CRAWLERS.append(crawler_obj)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)

    crawler.crawl()


# blocks process; so always keep as the last statement
reactor.run()
