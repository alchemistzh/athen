#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import requests
from wild.eastmoney import get_core_conception
from .mongodb import col_stock_profile, col_subject


def pull_and_save(code, name):
    cc = get_core_conception(code)
    doc = {
        'name': name,
        'groups': [],
        'subjects': []
    }
    for i in cc:
        if i['gjc'] == '所属板块':
            doc['groups'] = i['ydnr'].split(' ')
            continue
        doc['subjects'].append({
            'title': i['gjc'],
            'content': i['ydnr']
        })
    col_subject.update_one(
        {'_id': code},
        {'$set': doc},
        upsert=True
    )


stock_profile_docs = col_stock_profile.find(projection=['name'])
for d in stock_profile_docs:
    try:
        pull_and_save(d['_id'], d['name'])
    except Exception as e:
        logging.warning(d['_id'], e)
        continue

    time.sleep(0.2)
