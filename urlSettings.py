# -*- coding: utf-8 -*-

# 爬取域名
DOMAIN = 'eastlady.cn'

# 爬虫名
""" URL爬虫模块名，不可变 """
SPIDER_NAME = 'DgUrlSpider'

# 减肥瘦身
GROUP_ID = '33'
# 情感生活
# GROUP_ID = '30'

MODULE = '999'

# 文章列表页起始爬取URL
START_LIST_URL = 'http://www.eastlady.cn/emotion/pxgx/1.html'

# 文章列表循环规则
LIST_URL_RULER_PREFIX = 'http://www.eastlady.cn/emotion/pxgx/'
LIST_URL_RULER_SUFFIX = '.html'
LIST_URL_RULER_LOOP = 30

# 文章URL爬取规则XPATH
POST_URL_XPATH = '//div[@class="article_list"]/ul/li/span[1]/a[last()]/@href'
#
#
# def __init__():
#     print("=========== Stat urlSettings.py INIT() ===========")


