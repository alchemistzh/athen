#!/usr/bin/env python3
# coding: utf-8

import pymongo

from wild.eastmoney import query_shareholders


db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
COL = 'stock_profile'
stock_profiles = db[COL].find({})
for sp in stock_profiles:
    shareholders = query_shareholders(sp['_id'])
    print(sp._id)
    print(shareholders.restricted)
