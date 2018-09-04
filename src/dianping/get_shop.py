import urllib.request
import http.cookiejar
import pymysql
import json
from urllib import parse
from bs4 import BeautifulSoup

db = pymysql.connect("182.254.131.31", "test", "test", "test_dianping")
cursor = db.cursor()


def get_shop():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    more_url = "http://www.dianping.com/nanjing/ch10/p"
    cookie = http.cookiejar.MozillaCookieJar("loginCookie.txt")
    cookie.load('loginCookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    p = 1

    for i in range(1, 51):
        request = urllib.request.Request(url=more_url + str(i), headers=headers)
        with opener.open(request) as response:
            shop = response.read()
            cookie.save(ignore_discard=True, ignore_expires=True)
        shop = BeautifulSoup(shop, "lxml")
        shop = shop.find_all("a", onclick="LXAnalytics('moduleClick', 'shoppic')")
        for item in shop:
            n = item.attrs['data-shopid']
            cursor.execute("INSERT INTO shopInfo (shop_id,visit) VALUES(?,0)", n)
        db.commit()
        print(i)


get_shop()
db.close()
