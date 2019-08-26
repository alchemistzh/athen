#!/usr/bin/env python3
# coding: utf-8

import logging
import requests
import time
from datetime import datetime

import pymongo

from wild.xueqiu.stock_profile import get_stock_profile
from .mongodb import col_stock_profile


def pull_and_save(session, code):
    p = get_stock_profile(session, code)
    doc = dict(
        market_capital=p['market_capital'],
        float_market_capital=p['float_market_capital'],
        pb=p['pb'],
        pe_lyr=p['pe_lyr'],
        pe_ttm=p['pe_ttm'],
        pe_forecast=p['pe_forecast'],
        eps=p['eps'],
        dividend=p['dividend'],
        dividend_yield=p['dividend_yield'],
        total_shares=p['total_shares'],
        float_shares=p['float_shares'],
        high_52_week=p['high52w'],
        low_52_week=p['low52w'],
        price=p['last_close'],
        avg_price=p['avg_price'],
        volume=p['volume'],
        volume_ratio=p['volume_ratio'],
        amount=p['amount'],
        change=p['percent'],
        amplitude=p['amplitude'],
        update_time=datetime.now()
    )
    col_stock_profile.update_one(
        {'_id': code},
        {'$set': doc},
        upsert=True
    )


s = requests.Session()
stock_profile_docs = col_stock_profile.find(projection=[])
for d in stock_profile_docs:
    try:
        pull_and_save(s, d['_id'])
    except Exception as e:
        logging.warning(d['_id'], e)
        continue

    # time.sleep(0.1)
