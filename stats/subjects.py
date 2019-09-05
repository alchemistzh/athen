#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging

from stats.mongodb import col_stock_profile, col_shareholder, col_subject, col_finance
from stats.proportion import order_by_fund_proportion

cur_date = '2019-06-30'
prev_date = '2019-03-31'


def has_subject_and(doc, core, detail) -> bool:
    for c in core:
        if c not in doc['core']:
            return False
    for d in detail:
        if d not in doc['detail']:
            return False
    return True


def has_subject_or(doc, core, detail) -> bool:
    for c in core:
        if c in doc['core']:
            return True
    for d in detail:
        if d in doc['detail']:
            return True
    return False


def has_gjd(shareholder_doc) -> bool:
    if cur_date in shareholder_doc and 'float' in shareholder_doc[cur_date]:
        for h in shareholder_doc[cur_date]['float']:
            if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
                return True
    if prev_date in shareholder_doc and 'float' in shareholder_doc[prev_date]:
        for h in shareholder_doc[prev_date]['float']:
            if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
                return True
    return False


YI = 100000000
MAX_MARKET_CAPITAL = 10000*YI
MIN_MARKET_CAPITAL = 0*YI
SUBJECT_CORE = ['铁路基建']
SUBJECT_DETAIL = []


def filter_profile(doc):
    cap = doc['market_capital']
    if MIN_MARKET_CAPITAL < cap < MAX_MARKET_CAPITAL:
        return True
    return False


def filter_finance_indicator(fi_doc):
    reports = fi_doc['reports']
    if reports[0]['net_profit_yoy'] < 0:
        return False
    # if len(reports) > 2 and reports[2]['net_profit_yoy'] < 0:
    #     return False
    return True


if __name__ == '__main__':
    stock_profile_docs = []
    subject_docs = col_subject.find()
    for d in subject_docs:
        if not has_subject_or(d, SUBJECT_CORE, SUBJECT_DETAIL):
            continue
        profile_doc = col_stock_profile.find_one({'_id': d['_id']})
        if not filter_profile(profile_doc):
            continue
        finance_doc = col_finance.find_one({'_id': d['_id']})
        if not filter_finance_indicator(finance_doc):
            continue
        stock_profile_docs.append(profile_doc)
    order_by_fund_proportion(stock_profile_docs)
