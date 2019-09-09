#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging

from stats.mongodb import col_stock_profile, col_shareholder, col_subject, col_finance
from stats.proportion import sort_by_fund_proportion

cur_date = '2019-06-30'
prev_date = '2019-03-31'


def has_subject_and(doc, core, detail) -> bool:
    for c in core:
        if c not in doc['core']:
            return False
    for d in detail:
        for item in doc['detail']:
            if d not in item['title'] and d not in item['content']:
                return False
    return True


def has_subject_or(doc, core, detail) -> bool:
    for c in core:
        if c in doc['core']:
            return True
    for d in detail:
        for item in doc['detail']:
            if d in item['title'] or d in item['content']:
                doc['title'] = item['title']
                return True
    return False


YI = 100000000
MAX_MARKET_CAPITAL = 10000*YI
MIN_MARKET_CAPITAL = 0*YI


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


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-c', '--core', help='core', type=str, default='')
parser.add_argument('-d', '--detail', help='detail', type=str, default='')
args = parser.parse_args()


if __name__ == '__main__':
    subject_core = []
    if args.core:
        subject_core = args.core.split(',') if ',' in args.core else [args.core]
    subject_detail = []
    if args.detail:
        subject_detail = args.detail.split(',') if ',' in args.detail else [args.detail]

    stock_profile_docs = []
    subject_docs = col_subject.find()
    for d in subject_docs:
        if not has_subject_or(d, subject_core, subject_detail):
            continue
        profile_doc = col_stock_profile.find_one({'_id': d['_id']})
        # if not filter_profile(profile_doc):
        #     continue
        # finance_doc = col_finance.find_one({'_id': d['_id']})
        # if not filter_finance_indicator(finance_doc):
        #     continue
        stock_profile_docs.append(profile_doc)
    sort_by_fund_proportion(stock_profile_docs)
