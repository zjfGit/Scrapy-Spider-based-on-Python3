import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy
from DgSpider.items import DgspiderUrlItem
from scrapy.selector import Selector
from DgSpider import urlSettings


class DgUrlSpider(scrapy.Spider):
    print(">>>>>> Strarting DgUrlSpider:")

    # 爬虫名 必须静态指定
    # name = urlSettings.SPIDER_NAME
    name = 'DgUrlSpider'

    # 设定域名
    allowed_domains = [urlSettings.DOMAIN]

    # 爬取地址
    url_list = []
    """一般来说，列表页第一页不符合规则，单独append"""
    url_list.append(urlSettings.START_LIST_URL)
    loop = urlSettings.LIST_URL_RULER_LOOP
    for i in range(1, loop):
        url = urlSettings.LIST_URL_RULER_PREFIX + str(i) + urlSettings.LIST_URL_RULER_SUFFIX
        url_list.append(url)
    start_urls = url_list

    # 爬取方法
    def parse(self, response):

        # sel : 页面源代码
        sel = Selector(response)

        item_url = DgspiderUrlItem()
        url_item = []

        # XPATH获取url
        url_list = sel.xpath(urlSettings.POST_URL_XPATH).extract()

        # 消除http前缀差异
        for url in url_list:
            url = url.replace('http:', '')
            url_item.append('http:' + url)

        # list去重
        url_item = list(set(url_item))
        item_url['url'] = url_item

        yield item_url


print(">>>>>>>>>>>>> Starting DOUGUO Spider robot:")
url_spider = DgUrlSpider()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(url_spider)
process.start()

print(">>>>>>>>>>>>> Ending DOUGUO Spider robot:")
