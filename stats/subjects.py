#!/usr/bin/env python3
# coding: utf-8

import logging

from stats.mongodb import col_stock_profile, col_shareholder, col_subject, col_finance
from stats.proportion import fund_proportion_by_order

cur_date = '2019-06-30'
prev_date = '2019-03-31'


def has_group_and(doc, groups) -> bool:
    for g in groups:
        if g in doc['groups']:
            return False
    return True


def has_group_or(doc, groups) -> bool:
    for g in groups:
        if g in doc['groups']:
            return True
    return False


def has_subjects(doc, targets) -> bool:
    for t in targets:
        found_t = False
        for sub in doc['subjects']:
            if t in sub['title']:
                found_t = True
                break
        if not found_t:
            return False
    return True


def has_gjd(shareholder_doc) -> bool:
    if cur_date in shareholder_doc and 'float' in shareholder_doc[cur_date]:
        for h in shareholder_doc[cur_date]['float']:
            if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
                return True
    if prev_date in shareholder_doc and 'float' in shareholder_doc[prev_date]:
        for h in shareholder_doc[prev_date]['float']:
            if '中央汇金' in h['name'] or '中国证券金融' in h['name'] or '社保' in h['name']:
                return True
    return False


YI = 100000000


def filter_profile(doc):
    return True
    cap = doc['market_capital']
    if 10*YI < cap < 200*YI:
        return True
    return False


def filter_finance_indicator(fi_doc):
    reports = fi_doc['reports']
    if reports[0]['net_profit_yoy'] < 30:
        return False
    if len(reports) > 2 and reports[2]['net_profit_yoy'] < 0:
        return False
    return True


stock_profile_docs = []
subject_docs = col_subject.find()
for d in subject_docs:
    if not has_group_or(d, ['一带一路', '铁路基建']):
        continue
    profile_doc = col_stock_profile.find_one({'_id': d['_id']})
    if not filter_profile(profile_doc):
        continue
    finance_doc = col_finance.find_one({'_id': d['_id']})
    if not filter_finance_indicator(finance_doc):
        continue
    stock_profile_docs.append(profile_doc)

    # shareholder_doc = col_shareholder.find_one({'_id': d['_id']})
    # if has_groups(d, ['5G概念', '军工']) and has_gjd(shareholder_doc):
    #     print(d['_id'], d['name'])

fund_proportion_by_order(stock_profile_docs)
