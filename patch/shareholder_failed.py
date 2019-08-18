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
    '603121',
    '603236',
    '603256',
    '603279',
    '603332',
    '603530',
    '603613',
    '603687',
    '603697',
    '603739',
    '603983',
    '002947',
    '002953',
    '002956',
    '002957',
    '002966',
    '300758',
    '300763',
    '300769',
    '300778',
    '300783',
    '300785',
    '300786',
    '603115',
    '603662',
    '002960'
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

    time.sleep(0.3)
