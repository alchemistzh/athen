#!/usr/bin/env python3
# coding: utf-8

import logging

from .mongodb import col_stock_profile, col_shareholder


cur_date = '2019-06-30'
prev_date = '2019-03-31'


def inspect_gdj(sh_doc):
    cur = sh_doc[cur_date]
    prev = sh_doc[prev_date]
    # 最新十大流通股东中有国家队
    gjd_in_cur = False
    for h in cur['float']:
        if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
            gjd_in_cur = True
            break
    if not gjd_in_cur:
        return
    # 之前十大流通股东中没有国家队
    gjd_in_prev = False
    for h in prev['float']:
        if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
            gjd_in_prev = True
            break

    if not gjd_in_prev:
        print(sh_doc['_id'], sh_doc['name'])


shareholder_docs = col_shareholder.find()
for sh in shareholder_docs:
    if cur_date not in sh \
       or prev_date not in sh \
       or 'float' not in sh[cur_date]:
        continue
    try:
        inspect_gdj(sh)
    except Exception as e:
        logging.error(sh['_id'], e)
