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
    doc = dict(
        reports=[
            dict(
                report_name=fi['report_name'],
                report_date=datetime.fromtimestamp(int(fi['report_date'])/1000),
                revenue=fi['total_revenue'][0],
                net_profit=fi['net_profit_atsopc'][0],
                eps=fi['basic_eps'][0]
            ) for fi in fi_data['list']
        ],
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
        break
    except Exception as e:
        logging.warning(d['_id'], e)
        continue
