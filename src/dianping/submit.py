import urllib.request
import http.cookiejar
import json
from urllib import parse
from bs4 import BeautifulSoup
import pymysql
import random
import review


def re_submit(shop_id, review_body, food_feature):
    price = random.randint(30, 100)
    url = 'http://www.dianping.com/ajax/json/review/reviewAction'
    post_body = {
        "shopId": shop_id,
        "shopType": 10,
        "cityId": 5,
        "star":
            {
                "title": "总体评价",
                "value": 50,
                "desc": "超赞"
            },
        "scoreList": [{"title": "口味",
                       "value": 4,
                       "desc": "超棒"},
                      {"title": "环境",
                       "value": 4,
                       "desc": "超棒"
                       },
                      {"title": "服务",
                       "value": 4,
                       "desc": "超棒"}],
        "reviewBody": review_body,
        "expenseInfoList": [{"title": "人均",
                             "value": price,
                             "desc": "元"}],
        "extInfoList": [{"title": "停车信息",
                         "values": ["有停车"]},
                        {"title": "喜欢的菜",
                         "values": food_feature["like_food"]},
                        {"title": "餐厅特色",
                         "values": food_feature["feature"]}],
        "reviewPics": []
    }
    # print(post_body)
    post_body = json.dumps(post_body, ensure_ascii=False)
    # print(post_body)
    data = {
        "run": "a",
        "mode": "pro",
        "info": post_body,
        "reviewId": -1,
        "referPage": "http: //www.dianping.com/shop/" + shop_id,
    }
    data = parse.urlencode(data).encode('utf-8')
    headers = {
        'Accept': 'application/json, */*',
        'Accept-Encoding': 'gzip, deflate',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Origin": "http://www.dianping.com",
        "Referer": "http://www.dianping.com/shop/" + shop_id + "/review",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # 'X-Request': "JSON"
    }
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('loginCookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url=url, headers=headers, data=data)
    with opener.open(request) as response:
        html = response.read()
    soup = BeautifulSoup(html, "lxml")
    print(soup)
    # fp = open("test.htm", "w+b")  # 打开一个文本文件
    # fp.write(html)  # 写入数据
    # fp.close()  # 关闭文件


db = pymysql.connect("182.254.131.31", "", "", "test_dianping")
cursor = db.cursor()
cursor.execute("SELECT * FROM shopInfo WHERE visit = 0 LIMIT 10")
data = cursor.fetchall()
shop_list = []
for item in data:
    shop_list.append(item[1])
print(shop_list)

for shop_id in shop_list:
    re_body = review.get_rev_body(shop_id)
    re_p = review.get_food(shop_id)
    re_submit(shop_id, re_body, re_p)
    cursor.execute("UPDATE shopInfo SET visit = 1 WHERE shop_id = %s ", shop_id)
    db.commit()
