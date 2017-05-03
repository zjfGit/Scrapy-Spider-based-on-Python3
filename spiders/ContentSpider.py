# -*- coding: utf-8 -*-

import scrapy
from DgSpider.mysqlUtils import dbhandle_geturl
from DgSpider.items import DgspiderPostItem
from scrapy.selector import Selector
from scrapy.http import Request
from DgSpider import contentSettings
from DgSpider import urlSettings
from DgSpider.mysqlUtils import dbhandle_update_status


class DgContentSpider(scrapy.Spider):
    print('Spider DgContentSpider Staring...')

    result = dbhandle_geturl(urlSettings.GROUP_ID)

    url = result[0]
    spider_name = result[1]
    site = result[2]
    gid = result[3]
    module = result[4]

    name = 'DgContentSpider'

    # 设定爬取域名范围
    allowed_domains = [site]

    # 爬取地址
    start_urls = [url]

    start_urls_tmp = []
    """构造分页序列，一般来说遵循规则 url.html,url_2.html,url_3.html，并且url.html也写为url_1.html"""
    for i in range(6, 1, -1):
        start_single = url[:-5]
        start_urls_tmp.append(start_single+"_"+str(i)+".html")

    # 更新状态
    """对于爬去网页，无论是否爬取成功都将设置status为1，避免死循环"""
    dbhandle_update_status(url, 1)

    # 爬取方法
    def parse(self, response):
        item = DgspiderPostItem()

        # sel : 页面源代码
        sel = Selector(response)

        item['url'] = DgContentSpider.url

        # 对于title, <div><h1><span aaa><span>标题1</h1></div>,使用下列方法取得
        data_title_tmp = sel.xpath(contentSettings.POST_TITLE_XPATH)
        item['title'] = data_title_tmp.xpath('string(.)').extract()

        item['text'] = sel.xpath(contentSettings.POST_CONTENT_XPATH).extract()

        yield item

        if self.start_urls_tmp:
            url = self.start_urls_tmp.pop()
            yield Request(url, callback=self.parse)
