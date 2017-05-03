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

    # 爬虫名 必须静态指定
    # name = contentSettings.SPIDER_NAME
    name = 'DgContentSpider'

    # 设定爬取域名范围
    allowed_domains = [site]

    # 爬取地址
    # start_urls = ['http://www.mama.cn/baby/art/20140829/774422.html']
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

    # def start_requests(self):
    #     pages = []
    #     gid = contentSettings.GROUP_ID
    #     url_tmp = dbhandle_geturl(gid)
    #     start_single = url_tmp[:-5]
    #     print("=========== START URL ============")
    #     pages.append(url_tmp)
    #     for i in range(1, 10):
    #         url = start_single+"_"+str(i)+".html"
    #         # url='http://www.example.com/?page=%s'%i
    #         print(url)
    #         page = scrapy.Request(url)
    #         pages.append(page)
    #     return pages

    # init: 动态传入参数
    """命令行传参写法：  scrapy crawl MySpider -a start_url="http://www.lifeskill.cn/Html_qz_huaiyun/2015/2015072724958.shtml"""
    """
    def __init__(self,*args,**kwargs):
        super(DgPostSpider,self).__init__(*args,**kwargs)
        self.start_urls.append(kwargs.get('start_url'))
        for i in range(1, 6):
            start_single_tmp = kwargs.get('start_url')
            start_single = start_single_tmp[:-5]
            self.start_urls.append(start_single+"_"+str(i)+".html")
        print("=========ALL PAGES==========")
        print(self.start_urls)
        # self.start_urls = [kwargs.get('start_url')]
    """

    """此网站不存在翻页，方法废弃
    def getUrl(self, response):
        url_list = []
        select = Selector(response)
        page_list_tmp = select.xpath('//div[@class="viewnewpages"]/a[not(@class="next")]/@href').extract()
        for page_tmp in page_list_tmp:
            if page_tmp not in url_list:
                url_list.append("http://www.nvsheng.com/emotion/px/" + page_tmp)
        return url_list
    """