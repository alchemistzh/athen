#!/usr/bin/env python3
# coding: utf-8

"""
从深交所官网下载深市股票列表 xlsx 文件, 读取并存入 MongoDB.
"""

import logging
import requests
from collections import namedtuple
from typing import List

import xlrd

log = logging.getLogger(__name__)


def is_downloadable(url) -> bool:
    """
    Does the url contain a downloadable resource?
    """
    content_type = requests.head(url, allow_redirects=True).headers.get('content-type')
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False
    return True


stock = namedtuple('stock',
    [
        'code',          # 6 位代码
        'name',          # 简称
        'total_shares',  # 总股本
        'float_shares',  # 流通股本
    ]
)

def get_stock_list() -> List[stock]:
    """
    下载 http://www.szse.cn/market/stock/list/index.html 页面的股票列表 xlsx 文件并读取
    """
    url = 'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1'
    resp = requests.get(url)
    if not resp.ok:
        log.error("request failed: url=%s, response=%s", url, resp)
        exit(-1)
    wb = xlrd.open_workbook(file_contents=resp.content)
    st = wb.sheet_by_index(0)
    stock_list = []
    for i in range(1, st.nrows):
        row = st.row(i)
        stock_list.append(stock(
            code=row[5].value,
            name=row[6].value,
            total_shares=int(row[8].value.replace(',', '').strip()),
            float_shares=int(row[9].value.replace(',', '').strip())
        ))
    return stock_list


if __name__ == '__main__':
    stock_list = get_stock_list()
    print(len([s.code for s in stock_list]))
    s = stock_list[0]
    print(s._asdict())
