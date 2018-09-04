import urllib.request
import http.cookiejar
import json
from urllib import parse
from bs4 import BeautifulSoup
import time

url = "https://account.dianping.com/account/getqrcodeimg"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

cookie = http.cookiejar.MozillaCookieJar("loginCookie.txt")
handler = urllib.request.HTTPCookieProcessor(cookie)
request = urllib.request.Request(url=url, headers=headers)
opener = urllib.request.build_opener(handler)
with opener.open(request) as response:
    qrc = response.read()
    print("扫描二维码登陆")
cookie.save(ignore_discard=True, ignore_expires=True)
fp = open("qrc.png", "w+b")  # 打开一个文本文件
fp.write(qrc)
fp.close()
lgtoken = ""
for item in cookie:
    if item.name == "lgtoken":
        lgtoken = item.value


def login():
    while True:
        time.sleep(1)
        checkUrl = "https://account.dianping.com/account/ajax/queryqrcodestatus"
        postData = {
            "lgtoken": lgtoken
        }
        # cookie1 = http.cookiejar.MozillaCookieJar("loginCookie1.txt")
        # handler1 = urllib.request.HTTPCookieProcessor(cookie1)
        postData = parse.urlencode(postData).encode('utf-8')
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(url=checkUrl, headers=headers, data=postData)
        with opener.open(request) as response:
            status = response.read().decode("utf8")
            status = json.loads(status)
        # print(status[0])
        if status["msg"]["status"] == 2:
            cookie.save(ignore_discard=True, ignore_expires=True)
            print("登陆成功！")
            return
        else:
            print(status)


login()
