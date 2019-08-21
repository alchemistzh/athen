#!/usr/bin/env python3
# coding: utf-8

import logging

from .mongodb import col_shareholder, col_subject


cur_date = '2019-06-30'
prev_date = '2019-03-31'


def has_subjects(doc, subjects) -> bool:
    for sub in subjects:
        if sub not in doc['groups']:
            return False
    return True


def has_gjd(shareholder_doc) -> bool:
    if cur_date in shareholder_doc and 'float' in shareholder_doc[cur_date]:
        for h in shareholder_doc[cur_date]['float']:
            if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
                return True
    for h in shareholder_doc[prev_date]['float']:
        if '中央汇金' in h['name'] or '中国证券金融' in h['name']:
            return True
    return False


subject_docs = col_subject.find()
for d in subject_docs:
    shareholder_doc = col_shareholder.find_one({'_id': d['_id']})
    if has_subjects(d, ['5G概念', '军工']) and has_gjd(shareholder_doc):
        print(d['_id'], d['name'])
