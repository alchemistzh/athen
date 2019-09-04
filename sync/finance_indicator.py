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
    fi_data = get_finance_indicator(code, ReportType.All, 12)
    doc = dict(
        reports=[
            dict(
                report_name=fi['report_name'],
                report_date=datetime.fromtimestamp(int(fi['report_date'])/1000),
                revenue=fi['total_revenue'][0],
                revenue_yoy=fi['operating_income_yoy'][0],
                net_profit=fi['net_profit_atsopc'][0],
                net_profit_yoy=fi['net_profit_atsopc_yoy'][0],
                net_profit_after_nrgal=fi['net_profit_after_nrgal_atsolc'][0],
                net_profit_after_nrgal_yoy=fi['np_atsopc_nrgal_yoy'][0],
                eps=fi['basic_eps'][0],
                navps=fi['np_per_share'][0],
                udpps=fi['undistri_profit_ps'][0],
                capital_reserve=fi['capital_reserve'][0]
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
    except Exception as e:
        logging.warning(d['_id'], e)
        continue
    time.sleep(0.1)
