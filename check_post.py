import requests, re
import http
import urllib

# 圈圈：孕妈育儿 4
# 圈圈：减肥瘦身 33
# 圈圈：情感生活 30


def checkPost():
    # CREATE_POST_URL = "http://api.qa.douguo.net/robot/handlePost"
    CREATE_POST_URL = "http://api.douguo.net/robot/handlePost"

    fields={'group_id': '30',
            'type': 1,
            'apisign':'99ea3eda4b45549162c4a741d58baa60'}

    r = requests.post(CREATE_POST_URL, data=fields)

    print(r.json())

def testText(text):
    pic_flag_re = re.search('(.*)\001',text,re.M|re.I)
    return pic_flag_re.group(1)
    #return text.split('\001')

def test():
    url = 'http://qg.nrsfh.com/hwq/5078.html'
    start_urls_tmp = []
    for i in range(6, 0, -1):
        start_single = url[:-5]
        start_urls_tmp.append(start_single+"_"+str(i)+".html")
    print(start_urls_tmp)

def requestIp(ip):
    CREATE_POST_URL_alibaba = 'http://ip.taobao.com/service/getIpInfo.php?ip=[%s]' % ip
    CREATE_POST_URL_sina = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?ip=%s' % ip
    r = requests.post(CREATE_POST_URL_alibaba)
    response = urllib.urlopen(CREATE_POST_URL_alibaba)
    print(response.read())


if __name__ == '__main__':
    #for i in range(1,50):
    #checkPost()
    requestIp('58.132.171.18')
    #    print(i),
    #print(testText('aaaa\001'))