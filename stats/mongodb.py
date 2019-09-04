#!/usr/bin/env python3
# coding: utf-8

import pymongo


URI = 'mongodb://localhost:27017'
DB_ATHEN = 'athen'
db = pymongo.MongoClient(URI)[DB_ATHEN]

col_stock_profile = db['stock_profile']
col_shareholder = db['shareholder']
col_subject = db['subject']
col_finance = db['finance']
