#!/usr/bin/env python3
# coding: utf-8

from .mongodb import col_stock_profile


stock_profile_docs = col_stock_profile.find(projection=['name'])
for d in stock_profile_docs:
    name = d['name']
    if '华' == name[0] and '科技' in name:
        print(d['_id'], d['name'])
