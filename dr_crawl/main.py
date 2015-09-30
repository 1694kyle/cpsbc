from dr_crawl.spiders.dr_spider import DrSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(DrSpider)
process.start()

# todo: make sure settings defined in .cfg file