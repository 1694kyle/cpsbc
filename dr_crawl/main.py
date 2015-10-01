from dr_crawl.spiders.dr_spider import DrSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
import os



process = CrawlerProcess(get_project_settings())
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    for postal_code in postal_codes:
        for radius in xrange(1, 3):
            form_data = {
                'postal_code': postal_code,
                'radius': str(radius)
            }
            spider = DrSpider(kwargs=form_data)
            yield runner.crawl(spider)
    reactor.stop()


crawl()
reactor.run()



# process.crawl(DrSpider, form_data)
# process.start()

# todo: make sure settings defined in .cfg file