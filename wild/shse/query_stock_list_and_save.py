#!/usr/bin/env python3
# coding: utf-8

"""
Query stock list and save to MongoDB.
"""

from datetime import datetime

import pymongo

from stock_list import get_stock_list


db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
COLLECTION = 'stock_profile'

stock_list = get_stock_list()
operations = [
    pymongo.UpdateOne(
        {'_id': stock.code},
        {'$set': {
            'name': stock.name,
            'shares': stock.shares,
            'float_shares': stock.float_shares,
            'update_time': datetime.now(),
        }},
        upsert=True
    )
    for stock in stock_list
]
db[COLLECTION].bulk_write(operations)
