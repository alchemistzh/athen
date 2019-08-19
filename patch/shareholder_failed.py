#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime
from pprint import pprint

import pymongo

from wild.eastmoney import shareholder_research, get_main_positions


db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
stock_profiles = db['stock_profile'].find({})
col_shareholder = db['shareholder']

failed_codes = [
    '603308'
]

for code in failed_codes:
    try:
        shareholders = shareholder_research(code)
        shareholders['update_time'] = datetime.now()
        col_shareholder.update_one(
            {'_id': code},
            {'$set': shareholders},
            upsert=True
        )
    except Exception as e:
        logging.warning(code, e)
        continue

    time.sleep(0.1)
