#!/usr/bin/env python3
# coding: utf-8

"""
雪球个股首页报价信息接口

返回数据格式:
    见 samples/stock_profile.json
"""

import requests
import sys
from wild.xueqiu.cookie import get_cookies
from wild.util import parse_percent, str_to_int


session = requests.Session()
cookies = None


def get_stock_profile(stock_code):
    """
    stock_code -- 6 位股票代码
    """
    global cookies
    if cookies is None:
        cookies = get_cookies(session)
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
    resp = session.get(url, params=params, headers=headers, cookies=cookies)
    return resp.json()['data']['quote']


if __name__ == '__main__':
    print(get_stock_profile('600739'))
