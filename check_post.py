import requests, re
import http
import urllib


def checkPost():
    # 调用上传帖子接口
    CREATE_POST_URL = "http://api.test.net/robot/handlePost"

    fields={'group_id': '30',
            'type': 1,
            'apisign':'99ea3esdg45549162c4a741d58baa60'}

    r = requests.post(CREATE_POST_URL, data=fields)

    print(r.json())
