#!/usr/bin/env python3
# coding: utf-8

import pymongo

from db import col_stock_profile, col_subject


subject_docs = col_subject.find()
operations = [
    pymongo.UpdateOne(
        {'_id': sub['_id']},
        {'$set': {
            'subject': sub['core']
        }},
    )
    for sub in subject_docs
]

col_stock_profile.bulk_write(operations)
