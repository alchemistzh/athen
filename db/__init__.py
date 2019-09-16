#!/usr/bin/env python3
# coding: utf-8

import pymongo


URI = 'mongodb://localhost:27017'
DATABASE = 'athen'

cli = pymongo.MongoClient(URI)[DATABASE]

col_stock_profile = cli['stock_profile']
col_shareholder = cli['shareholder']
col_subject = cli['subject']
col_finance = cli['finance']
