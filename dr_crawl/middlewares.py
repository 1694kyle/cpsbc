
from scrapy.http import HtmlResponse
from selenium import webdriver


class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        if request.url == spider.search_url and spider.name == 'dr_spider':
            driver = webdriver.PhantomJS()
            postal_code = spider.postal_code
            radius = spider.radius

            driver.get(request.url)

            postal_code_field = driver.find_element_by_name('filter[postal_code]')
            radius_field = driver.find_element_by_name('filter[radius]')
            search_button = driver.find_element_by_xpath('//*[@id="edit-submit"]')

            postal_code_field.send_keys(postal_code)
            radius_field.send_keys(radius)
            search_button.click()

            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return None