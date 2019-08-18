#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import pymongo

from wild.eastmoney import shareholder_research, get_main_positions
from sync.mongodb import col_stock_profile, col_shareholder


stock_profile_docs = col_stock_profile.find(projection=['name'])
operations = [
    pymongo.UpdateOne(
        {'_id': p['_id']},
        {'$set': {
            'name': p['name']
        }},
    )
    for p in stock_profile_docs
]

col_shareholder.bulk_write(operations)
