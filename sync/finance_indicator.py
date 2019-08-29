#!/usr/bin/env python3
# coding: utf-8

import logging
import requests
import time
from datetime import datetime

import pymongo

from wild.xueqiu.finance_indicator import get_finance_indicator, ReportType
from .mongodb import col_stock_profile, col_finance


def pull_and_save(code):
    fi_data = get_finance_indicator(code, ReportType.Q4, 10)
    for fi in fi_data['list']:
        doc = dict(
            report_name=fi['report_name'],
            report_date=datetime.fromtimestamp(int(fi['report_date'])/1000).date(),
            update_time=datetime.now()
        )
        col_finance.update_one(
            {'_id': code},
            {'$set': doc},
            upsert=True
        )


stock_profile_docs = col_stock_profile.find(projection=[])
for d in stock_profile_docs:
    try:
        pull_and_save(d['_id'])
    except Exception as e:
        logging.warning(d['_id'], e)
        continue
