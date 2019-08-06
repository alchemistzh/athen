#!/usr/bin/env python3
# coding: utf-8

"""
从深交所官网下载深市股票列表 xlsx 文件, 读取并存入 MongoDB.
"""

import logging
import requests

import pymongo
import xlrd

log = logging.getLogger(__name__)


def is_downloadable(url) -> bool:
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


url = 'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1'
resp = requests.get(url)
if not resp.ok:
    log.error("request failed: url=%s, response=%s", url, resp)
    exit(-1)


db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
COLLECTION = 'stock_profile'
operations = []

wb = xlrd.open_workbook(file_contents=resp.content)
st = wb.sheet_by_index(0)
for i in range(1, st.nrows):
    row = st.row(i)
    code = row[5].value
    data = {
        '_id': code,
        'name': row[6].value,
        'shares': int(row[8].value.replace(',', '').strip()),
        'float_shares': int(row[9].value.replace(',', '').strip())
    }
    operations.append(pymongo.UpdateOne(
        {'_id': code},
        {'$set': data},
        upsert=True
    ))

db[COLLECTION].bulk_write(operations)
