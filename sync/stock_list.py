#!/usr/bin/env python3
# coding: utf-8

"""
Query stock list and save to MongoDB.
"""

from datetime import datetime

import pymongo

from wild.shse.stock_list import get_stock_list as sh_stock_list
from wild.szse.stock_list import get_stock_list as sz_stock_list


stock_list = sh_stock_list() + sz_stock_list()
operations = [
    pymongo.UpdateOne(
        {'_id': stock.code},
        {'$set': {
            'name': stock.name,
            'total_shares': stock.shares,
            'float_shares': stock.float_shares,
            'update_time': datetime.now(),
        }},
        upsert=True
    )
    for stock in stock_list
]

db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
COLLECTION = 'stock_profile'
db[COLLECTION].bulk_write(operations)
