# -*- coding: utf-8 -*-

# Define your item pipelines here
# If you have many piplelines, all should be init here
# and use IF to judge them
#
# DOUGUO Spider pipelines
# @author zhangjianfei
# @date 2017/04/13

import re
import urllib.request
from DgSpider import urlSettings
from DgSpider import contentSettings
from DgSpider.mysqlUtils import dbhandle_insert_content
from DgSpider.uploadUtils import uploadImage
from DgSpider.mysqlUtils import dbhandle_online
from DgSpider.mysqlUtils import dbhandle_update_status
from bs4 import BeautifulSoup
from DgSpider.PostHandle import post_handel
from DgSpider.commonUtils import get_random_user
from DgSpider.commonUtils import get_linkmd5id


class DgPipeline(object):
    # post构造reply
    cs = []

    # 帖子title
    title = ''

    # 帖子文本
    text = ''

    # 当前爬取的url
    url = ''

    # 随机用户ID
    user_id = ''

    # 图片flag
    has_img = 0

    # get title flag
    get_title_flag = 0

    def __init__(self):
        DgPipeline.user_id = get_random_user(contentSettings.CREATE_POST_USER)

    # process the data
    def process_item(self, item, spider):
        self.get_title_flag += 1

        # pipeline for content
        if spider.name == contentSettings.SPIDER_NAME:

            # 获取当前网页url
            DgPipeline.url = item['url']

            # 获取post title
            if len(item['title']) == 0:
                title_tmp = ''
            else:
                title_tmp = item['title'][0]

            # 替换标题中可能会引起 sql syntax 的符号
            # 对于分页的文章，只取得第一页的标题
            if self.get_title_flag == 1:

                # 使用beautifulSoup格什化标题
                soup_title = BeautifulSoup(title_tmp, "lxml")
                title = ''
                # 对于bs之后的html树形结构，不使用.prettify()，对于bs, prettify后每一个标签自动换行，造成多个、
                # 多行的空格、换行，使用stripped_strings获取文本
                for string in soup_title.stripped_strings:
                    title += string

                title = title.replace("'", "”").replace('"', '“')
                DgPipeline.title = title

            # 获取正post内容
            if len(item['text']) == 0:
                text_temp = ''
            else:
                text_temp = item['text'][0]

            # 获取图片
            reg_img = re.compile(r'<img.*>')
            imgs = reg_img.findall(text_temp)
            for img in imgs:
                DgPipeline.has_img = 1

                # matchObj = re.search('.*src="(.*)"{2}.*', img, re.M | re.I)
                match_obj = re.search('.*src="(.*)".*', img, re.M | re.I)
                img_url_tmp = match_obj.group(1)

                # 去除所有Http:标签
                img_url_tmp = img_url_tmp.replace("http:", "")

                # 对于<img src="http://a.jpg" title="a.jpg">这种情况单独处理
                imgUrl_tmp_list = img_url_tmp.split('"')
                img_url_tmp = imgUrl_tmp_list[0]

                # 加入http
                imgUrl = 'http:' + img_url_tmp

                list_name = imgUrl.split('/')
                file_name = list_name[len(list_name)-1]

                # if os.path.exists(settings.IMAGES_STORE):
                #     os.makedirs(settings.IMAGES_STORE)

                # 获取图片本地存储路径
                file_path = contentSettings.IMAGES_STORE + file_name
                # 获取图片并上传至本地
                urllib.request.urlretrieve(imgUrl, file_path)
                upload_img_result_json = uploadImage(file_path, 'image/jpeg', DgPipeline.user_id)
                # 获取上传之后返回的服务器图片路径、宽、高
                img_u = upload_img_result_json['result']['image_url']
                img_w = upload_img_result_json['result']['w']
                img_h = upload_img_result_json['result']['h']
                img_upload_flag = str(img_u)+';'+str(img_w)+';'+str(img_h)

                # 在图片前后插入字符标记
                text_temp = text_temp.replace(img, '[dgimg]' + img_upload_flag + '[/dgimg]')

            # 使用beautifulSoup格什化HTML
            soup = BeautifulSoup(text_temp, "lxml")
            text = ''
            # 对于bs之后的html树形结构，不使用.prettify()，对于bs, prettify后每一个标签自动换行，造成多个、
            # 多行的空格、换行
            for string in soup.stripped_strings:
                text += string + '\n'

            # 替换所有br符
            # strCpla = re.compile(r'<br[.]+>', re.S | re.I)
            # text = strCpla.sub('', text).replace("'", "")
            # text = text.replace('<br>', '\n').replace('<BR>', '\n').replace('<br/>', '\n').replace('<BR/>', '\n')
            # .replace('<br>', '\n')

            # 替换所有HTML标签
            # strCplb = re.compile(r'<[^>]+>', re.S | re.X)
            # text = strCplb.sub('', text).replace("'", "")

            # 替换因为双引号为中文双引号，避免 mysql syntax
            DgPipeline.text = self.text + text.replace('"', '“')

            # 对于分页的文章，每一页之间加入换行
            # DgPipeline.text += (DgPipeline.text + '\n')

        # pipeline for url
        elif spider.name == urlSettings.SPIDER_NAME:
            db_object = dbhandle_online()
            cursor = db_object.cursor()

            for url in item['url']:
                linkmd5id = get_linkmd5id(url)
                spider_name = contentSettings.SPIDER_NAME
                site = urlSettings.DOMAIN
                gid = urlSettings.GROUP_ID
                module = urlSettings.MODULE
                status = '0'
                sql_search = 'select md5_url from dg_spider.dg_spider_post where md5_url="%s"' % linkmd5id
                sql = 'insert into dg_spider.dg_spider_post(md5_url, url, spider_name, site, gid, module, status) ' \
                      'values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                      % (linkmd5id, url, spider_name, site, gid, module, status)
                try:
                    # 判断url是否存在,如果不存在，则插入
                    cursor.execute(sql_search)
                    result_search = cursor.fetchone()
                    if result_search is None or result_search[0].strip() == '':
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        db_object.commit()
                except Exception as e:
                    print(">>> catch exception !")
                    print(e)
                    db_object.rollback()

        return item

    # spider开启时被调用
    def open_spider(self, spider):
        pass

    # sipder 关闭时被调用
    def close_spider(self, spider):
        if spider.name == contentSettings.SPIDER_NAME:
            # 数据入库：235
            url = DgPipeline.url
            title = DgPipeline.title
            content = DgPipeline.text
            user_id = DgPipeline.user_id
            dbhandle_insert_content(url, title, content, user_id, DgPipeline.has_img)

            # 更新status状态为1（已经爬取过内容）
            """此项已在spider启动时设置"""
            # dbhandle_update_status(url, 1)

            # 处理文本、设置status、上传至dgCommunity.dg_post
            # 如果判断has_img为1，那么上传帖子
            if DgPipeline.has_img == 1:
                if title.strip() != '' and content.strip() != '':
                    spider.logger.info('has_img=1,title and content is not null! Uploading post into db...')
                    post_handel(url)
                else:
                    spider.logger.info('has_img=1,but title or content is null! ready to exit...')
                pass
            else:
                spider.logger.info('has_img=0, changing status and ready to exit...')
                pass

        elif spider.name == urlSettings.SPIDER_NAME:
            pass

