from dr_crawl.spiders.dr_spider import DrSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

postal_codes = [code.strip() for code in open('postal_codes')]

process = CrawlerProcess(get_project_settings())

for postal_code in postal_codes:
    for radius in xrange(1, 11):
        process.crawl(DrSpider, postal_code, str(radius))
        process.start()

# todo: make sure settings defined in .cfg file