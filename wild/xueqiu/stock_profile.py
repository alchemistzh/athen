#!/usr/bin/env python3
# coding: utf-8

"""
雪球个股首页报价信息接口

返回数据格式:
    见 samples/stock_profile.json
"""

import sys
import requests

from wild.util import parse_percent, str_to_int


# Save cookie at `this.cookies`
this = sys.modules[__name__]
this.cookies = None


def __get_cookie():
    """
    通过访问雪球主页获取 Cookie
    """
    url = 'https://xueqiu.com'
    headers = {
        'Accept': '*/*',
        'Host': 'xueqiu.com',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }
    resp = requests.get(url, headers=headers)
    return resp.cookies


def get_stock_profile(stock_code):
    """
    stock_code -- 6 位股票代码
    """
    if this.cookies is None:
        this.cookies = __get_cookie()

    code = '{}{}'.format('SH' if stock_code.startswith('6') else 'SZ', stock_code)
    url = 'https://stock.xueqiu.com/v5/stock/quote.json'
    params = {
        'symbol': code,
        'extend': 'detail',
    }
    headers = {
        'Accept': '*/*',
        'Referer': 'https://xueqiu.com/S/{}'.format(code),
        'Host': 'stock.xueqiu.com',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }
    resp = requests.get(url, params=params, headers=headers, cookies=this.cookies)
    return resp.json()['data']['quote']


if __name__ == '__main__':
    print(get_stock_profile('600739'))
