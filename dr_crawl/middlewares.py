
from scrapy.http import HtmlResponse
from selenium import webdriver


class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        driver = webdriver.Firefox()
        driver.get(request.url)

        # zip = spider.zip.next()
        # radius = spider.radius.next()

        postal_code = driver.find_element_by_name('filter[postal_code]')
        radius = driver.find_element_by_name('filter[radius]')
        search_button = driver.find_element_by_xpath('//*[@id="edit-submit"]')

        postal_code.send_keys('V5K 0A1')
        radius.send_keys('2')
        search_button.click()

        body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)