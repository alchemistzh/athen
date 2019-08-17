#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import pymongo

from wild.eastmoney import shareholder_research, get_main_positions


db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
stock_profiles = db['stock_profile'].find({})
col_shareholder = db['shareholder']

for sp in stock_profiles:
    try:
        shareholders = shareholder_research(sp['_id'])
        shareholders['update_time'] = datetime.now()
        col_shareholder.update_one(
            {'_id': sp['_id']},
            {'$set': shareholders},
            upsert=True
        )
    except Exception as e:
        logging.warning(sp['_id'], e)
        continue

    time.sleep(0.3)
