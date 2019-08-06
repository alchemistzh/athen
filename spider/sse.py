#!/usr/bin/env python3
# coding: utf-8

"""
Query stock list from sse.com.cn and save to MongoDB.

返回数据格式：
{
    "result": [
        {
            "COMPANY_CODE": "600000",
            "SECURITY_ABBR_A": "浦发银行",
            "SECURITY_ABBR_B": "-",
            "SECURITY_CODE_A": "600000",
            "SECURITY_CODE_B": "-",
            "totalShares": "2935208.04",
            "totalFlowShares": "2810376.39",
            "NUM": "1",
            "TYPE": "主板A股",
            "LISTING_DATE": "1999-11-10"
            "endDate": "2019-08-02",
        },
    ]
}
"""

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

import logging
import requests
import time
from typing import Dict, List

import backoff
import pymongo
from ratelimit import limits, sleep_and_retry

log = logging.getLogger(__name__)

# resp = requests.get(url, headers=headers, params=params)
# print(resp.json())
# exit(0)

db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
COLLECTION = 'stock_profile'


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=5)
def get_stock_list(page: int) -> List[Dict]:
    params['pageHelp.beginPage'] = page
    resp = requests.get(url, headers=headers, params=params)
    if not resp.ok:
        log.error("request failed: url=%s, response=%s", url, resp)
        return []
    r = resp.json()['result']
    return [
        {
            '_id': stock['SECURITY_CODE_A'].strip(),
            'name': stock['SECURITY_ABBR_A'].strip(),
        } for stock in r
    ]


while True:
    print(get_stock_list(1))


currentPage = 1
stock_list = []

while True:
    params['pageHelp.beginPage'] = currentPage
    currentPage += 1
    resp = requests.get(url, headers=headers, params=params)
    if not resp.ok:
        log.error("request failed: url=%s, response=%s", url, resp)
        break
    r = resp.json()['result']
    if len(r) == 0:
        break
    for stock in r:
        stock_list.append({
            '_id': stock['SECURITY_CODE_A'].strip(),
            'name': stock['SECURITY_ABBR_A'].strip(),
        })
    time.sleep(0.3)

db[COLLECTION].insert_many(stock_list)
