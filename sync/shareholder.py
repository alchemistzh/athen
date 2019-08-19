#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import pymongo

from wild.eastmoney import shareholder_research, get_main_positions
from .mongodb import col_stock_profile, col_shareholder


stock_profile_docs = col_stock_profile.find(projection=['name'])
for d in stock_profile_docs:
    try:
        shareholders = shareholder_research(d['_id'])
        shareholders['name'] = d['name']
        shareholders['update_time'] = datetime.now()
        col_shareholder.update_one(
            {'_id': d['_id']},
            {'$set': shareholders},
            upsert=True
        )
    except Exception as e:
        logging.warning(d['_id'], e)
        continue

    time.sleep(0.1)
