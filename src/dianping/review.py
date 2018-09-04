import urllib.request
import http.cookiejar
import json
from urllib import parse
from bs4 import BeautifulSoup


def get_rev_body(shop_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Referer": "https://www.dianping.com/shop/" + shop_id
    }
    more_url = "https://www.dianping.com/shop/" + shop_id + "/review_all/p2"
    cookie = http.cookiejar.MozillaCookieJar("loginCookie.txt")
    cookie.load('loginCookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url=more_url, headers=headers)
    with opener.open(request) as response:
        shop = response.read()
        cookie.save(ignore_discard=True, ignore_expires=True)
    shop = BeautifulSoup(shop, "lxml")
    shop = shop.find_all("div", class_="review-words Hide")
    rev_body = ""
    for item in shop:
        rev_body = item.get_text("|", strip=True)
        if len(rev_body) >= 110:
            rev_body = rev_body.replace("|收起评论", "")
    return rev_body


def get_food(shop_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Referer": "https://www.dianping.com/shop/" + shop_id
    }

    submit_url = "http://www.dianping.com/shop/" + shop_id + "/review"
    cookie = http.cookiejar.MozillaCookieJar("loginCookie.txt")
    cookie.load('loginCookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url=submit_url, headers=headers)
    with opener.open(request) as response:
        shop = response.read()
        cookie.save(ignore_discard=True, ignore_expires=True)
    shop = BeautifulSoup(shop, "lxml")
    result = {"like_food": [], "feature": []}
    shop = shop.find_all("div", class_="form-block taglist-block fb-fav")
    # print(len(shop))
    # print(shop)
    # shop[0].find_all("a", class_="chara-label")
    if len(shop) > 0:
        for item in shop[0].find_all("a", class_="chara-label"):
            result["like_food"] += item
    if len(shop) > 1:
        for item in shop[1].find_all("a", class_="chara-label"):
            result["feature"] += item
    return result

