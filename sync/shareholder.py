#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import pymongo

from wild.eastmoney import shareholder_research, get_main_positions
from .mongodb import col_stock_profile, col_shareholder


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
    except Exception as e:
        logging.warning(d['_id'], e)
        continue
