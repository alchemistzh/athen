#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import pymongo

from db import col_stock_profile, col_shareholder
from util.datetime import CURRENT_REPORT_DATE
from wild.eastmoney import shareholder_research, get_main_positions


def sum_total_proportion(doc):
    for total in doc['total'].values():
        p = 0.0
        for t in total['list']:
            p += t['proportion']
        total['proportion'] = p
    for float in doc['float'].values():
        p = 0.0
        for f in float['list']:
            p += f['proportion']
        float['proportion'] = p
    for fund in doc['fund'].values():
        p = 0.0
        for f in fund['list']:
            p += f['proportion']
        fund['proportion'] = p


def copy_proportion_to_stock_profile(stock_profile_doc, shareholder_doc):
    total = shareholder_doc['total'].get(CURRENT_REPORT_DATE)
    if total:
        stock_profile_doc['total_proportion'] = total['proportion']
    float = shareholder_doc['float'].get(CURRENT_REPORT_DATE)
    if float:
        stock_profile_doc['float_proportion'] = float['proportion']
    fund = shareholder_doc['fund'].get(CURRENT_REPORT_DATE)
    if fund:
        stock_profile_doc['fund_proportion'] = fund['proportion']


stock_profile_docs = col_stock_profile.find(projection=['name'])
for d in stock_profile_docs:
    try:
        doc = shareholder_research(d['_id'])
        doc['name'] = d['name']
        # doc['lastest_date'] = sorted(doc['total'].keys(), reverse=True)[0]
        doc['update_time'] = datetime.now()
        sum_total_proportion(doc)
        col_shareholder.update_one(
            {'_id': d['_id']},
            {'$set': doc},
            upsert=True
        )
        copy_proportion_to_stock_profile(d, doc)
        col_stock_profile.update_one(
            {'_id': d['_id']},
            {'$set': d},
        )
    except Exception as e:
        logging.warning(d['_id'], e)
        continue
