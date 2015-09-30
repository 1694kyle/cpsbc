from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, Request, Rule, CrawlSpider
from datetime import datetime
from scrapy.selector import Selector
from dr_crawl.items import DrCrawlItem
import pdb
import re
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

def load_xpaths():
    xpaths = {
        'title': './/span[@id="productTitle"]/text()',
        'asin': '',
        'lowest_used_price1': './/a[contains(text(),"Used")]/text()[2]',
        'lowest_new_price1': './/a[contains(text(),"New")]/text()[2]',
        'lowest_used_price2': './/span[a[contains(text(),"Used")]]/span/text()',
        'lowest_new_price2': './/span[a[contains(text(),"New")]]/span/text()',
        'trade_in_eligible': ' ',
        'trade_value': './/span[@id="tradeInButton_tradeInValue"]/text()',
        'url': ' ',
        'price': ' ',
        'profit': ' ',
        'profitable': ' '
    }
    return xpaths


def build_start_urls(pc_file='zips', **kwargs):
    urls = []
    pcs = ['%'.join(z.strip().split()) for z in open(pc_file)]
    for pc in pcs:
        urls.append(build_search_url(postal_code=pc))
    return urls


def build_search_url(**kwargs):
    base_url = r'https://www.cpsbc.ca/physician_search?' \
               r'filter_first_name={first_name}' \
               r'&filter_last_name={last_name}' \
               r'&filter_city={city}' \
               r'&filter_gp_or_spec={practice_type}' \
               r'&filter_specialty={specialty}' \
               r'&filter_accept_new_pat={accepting_new}' \
               r'&filter_gender={gender}' \
               r'&filter_active=A' \
               r'&filter_radius={radius}' \
               r'&filter_postal_code={postal_code}' \
               r'&filter_language=' \
               r'&filter_nonce=1113150886' \
               r'&e92faf8b732de6f565afa13d6e79b1d7=296'


    search_url = base_url.format(
        first_name=kwargs.get('first_name', ''),
        last_name=kwargs.get('last_name', ''),
        city=kwargs.get('city', ''),
        practice_type=kwargs.get('practice_type', 'A'),
        specialty=kwargs.get('specialty', ''),
        accepting_new=kwargs.get('accepting_new', 0),
        gender=kwargs.get('gender', 'E'),
        radius=kwargs.get('radius', ''),
        postal_code=kwargs.get('postal_code', ''),
     )

    # todo: only accepting new?
    return search_url


class DrSpider(CrawlSpider):
    name = 'dr_spider'
    allowed_domains = [r'www.cpsbc.ca']
    start_urls = build_start_urls()
    rules = (
        # parse dr info page
        Rule(
            LinkExtractor(allow=('/physician_search_result/',), restrict_xpaths=['//td[@class="title-address"]',]),
            callback="parse_dr_page",
            # follow=True
            ),

        # follow next page (link in "next" button)
        Rule(
            LinkExtractor(allow=('.+&page=\d+',), restrict_xpaths=['.//div[@class="pager inline item-list"]/li[contains(., "Next")]', ]),
            follow=True,
            ),
        )

    def __init__(self, *args, **kwargs):
        super(DrSpider, self).__init__(*args, **kwargs)
        self.name = 'dr_spider'
        self.item_xpaths = load_xpaths()
        self.start_urls = build_start_urls()

    # def parse_results_page(self, response):
    #     regex_title = re.compile(r'http://www.amazon.com/(.+)/dp')
    #     sel = Selector(response)
    #
    #     yield item

    def parse_dr_page(self, response):
            sel = Selector(response)
            item = DrCrawlItem()
            for name, path in self.item_xpaths.iteritems():
                try:
                    item[name] = sel.xpath(path).extract()[0].strip().replace(',', '').replace('$', '')
                except (KeyError, IndexError, ValueError):
                    item[name] = ' '

            item['url'] = response.url

            yield item

