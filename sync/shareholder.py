#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import pymongo

from wild.eastmoney import shareholder_research, get_main_positions
from .mongodb import col_stock_profile, col_shareholder


def sum_total_proportion(doc):
    for r in doc['report']:
        total_p, float_p = 0.0, 0.0
        for f in r['float']:
            float_p += f['proportion']
        for t in r['total']:
            total_p += t['proportion']
        r['float_proportion'] = float_p
        r['total_proportion'] = total_p


stock_profile_docs = col_stock_profile.find(projection=['name'])
for d in stock_profile_docs:
    try:
        doc = shareholder_research(d['_id'])
        doc['name'] = d['name']
        doc['lastest_date'] = doc['report'][0]['date']
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
