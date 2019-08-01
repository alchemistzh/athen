#!/usr/bin/env python3
# coding: utf-8

"""
Query stock list from sse.com.cn and save to MongoDB.
"""

import logging
import requests

url = 'http://query.sse.com.cn/security/stock/getStockListData.do'

headers = {
    'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

params = {
    'isPagination': 'true',
    'stockCode': '',
    'csrcCode': '',
    'areaName': '',
    'stockType': 1,  # 1: 主板A股  2: B股  8: 科创板
    'pageHelp.cacheSize': 1,
    'pageHelp.beginPage': 1,  # 页数， 每次请求递增
    'pageHelp.pageSize': 50,  # 每次请求返回的股票数量， 最大50
    'pageHelp.pageNo': 1,
}

resp = requests.get(url, headers=headers, params=params)
if not resp.ok:
    logging.getLogger(__name__).error("request failed: url=%s, response=%s", url, resp)

print(resp.json())
