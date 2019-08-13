#!/usr/bin/env python3
# coding: utf-8

import pymongo


db = pymongo.MongoClient('mongodb://localhost:27017')['athen']
COL = 'stock_profile'
stock_profiles = db[COL].find({})
for sp in stock_profiles:
    print(sp['_id'])
