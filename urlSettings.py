# -*- coding: utf-8 -*-

# 爬取域名
DOMAIN = 'eastlady.cn'

# 爬虫名
SPIDER_NAME = 'DgUrlSpider'

GROUP_ID = '33'

MODULE = '999'

# 文章列表页起始爬取URL
START_LIST_URL = 'http://www.eastlady.cn/emotion/pxgx/1.html'

# 文章列表循环规则
LIST_URL_RULER_PREFIX = 'http://www.eastlady.cn/emotion/pxgx/'
LIST_URL_RULER_SUFFIX = '.html'
LIST_URL_RULER_LOOP = 30

# 文章URL爬取规则XPATH
POST_URL_XPATH = '//div[@class="article_list"]/ul/li/span[1]/a[last()]/@href'

