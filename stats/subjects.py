#!/usr/bin/env python3
# coding: utf-8

import logging

from .mongodb import col_stock_profile, col_shareholder, col_subject


cur_date = '2019-06-30'
prev_date = '2019-03-31'


def has_groups(doc, groups) -> bool:
    for g in groups:
        if g not in doc['groups']:
            return False
    return True


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


def filter_profile(prifle_doc):
    if prifle_doc['market_capital'] <= 31 * 100000000:
        return True
    return False


subject_docs = col_subject.find()
for d in subject_docs:
    profile_doc = col_stock_profile.find_one({'_id': d['_id']})
    if not filter_profile(profile_doc):
        continue
    shareholder_doc = col_shareholder.find_one({'_id': d['_id']})
    if has_gjd(shareholder_doc) and has_subjects(d, ['汽车零部件']):
        print(d['_id'], d['name'])
    # if has_groups(d, ['5G概念', '军工']) and has_gjd(shareholder_doc):
    #     print(d['_id'], d['name'])
