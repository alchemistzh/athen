#!/usr/bin/env python3
# coding: utf-8

import logging
from typing import List

from stats.mongodb import col_shareholder
from util.datetime import REPORT_DATES


# big brohter 股东名
GJD = ['中央汇金', '中国证券金融']
DJJ = ['国家集成电路产业投资基金']
MANU = ['先进制造产业投资基金']
SB = ['社保基金']

def has_big_brother_in(shareholders: List, big_brothers: List, min_proportion=0.0) -> bool:
    """
    检查 big brother 是否在股东中

    shareholders   -- 股东列表
    big_brothers   -- big brother 列表
    min_proportion -- 最小持仓比例
    """
    for sh in shareholders:
        for bb in big_brothers:
            if bb in sh['name'] and sh['proportion'] >= min_proportion:
                return True
    return False


def inspect_big_brothers(doc, big_brothers):
    """
    检查并打印: 最新股东中有 big brother, 之前没有

    doc          -- shareholder document
    big_brothers -- big brother 列表
    """
    cur = doc['float'][REPORT_DATES[0]]
    prev = doc['float'][REPORT_DATES[1]]
    if has_big_brother_in(cur['list'][0:6], big_brothers, 1.0) and not has_big_brother_in(prev['list'], big_brothers):
        print(doc['_id'], doc['name'])


shareholder_docs = col_shareholder.find({})
for doc in shareholder_docs:
    float = doc.get('float')
    if not float:
        continue
    if not float.get(REPORT_DATES[0]) or not float.get(REPORT_DATES[1]):
        continue
    try:
        inspect_big_brothers(doc, GJD)
        inspect_big_brothers(doc, DJJ)
        inspect_big_brothers(doc, MANU)
        inspect_big_brothers(doc, SB)
    except Exception as e:
        logging.error(doc['_id'], e)
