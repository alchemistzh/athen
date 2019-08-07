#!/usr/bin/env python3
# coding: utf-8

"""
调用 <东方财富> web 接口获取股票股东情况:
    十大股东
    十大流通股东
    基金持股
"""

url = 'http://f10.eastmoney.com/ShareholderResearch/ShareholderResearchAjax'

headers = {
    "Referer": 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=SH600703',
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    "X-Requested-With": 'XMLHttpRequest',
}

params = {
    'code': 'SH600703',
}

import requests

resp = requests.get(url, headers=headers, params=params)
print(resp.json())
