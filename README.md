网页爬虫设计
====  

创建项目
-------  

 - 进入指定文件夹，右击空白处>在此处打开命令行窗口
 - 创建项目
```
Scrapy startproject DgSpider
```

主要代码文件说明
-------  

 - 爬虫主类  ：UrlSpider.py、ContentSpider.py
	 *项目包含2个爬虫主类，分别用于爬取文章列表页所有文章的URL、文章详情页具体内容*
 - 内容处理类 ：pipelines.py
	 *处理内容*
 - 传输字段类 ：items.py
	*暂存爬取的数据*
 - 设置文件 ：settings.py
	*用于主要的参数配置*
 - 数据库操作：mysqlUtils.py
	  *链接操作数据库*
 - 文本处理、上传文本：PostHandle.py
	  *处理文本*

