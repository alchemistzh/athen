#!/usr/bin/env python3
# coding: utf-8

import pymongo
from datetime import date, datetime
from pprint import pprint

from .mongodb import col_stock_profile
from wild.eastmoney import shareholder_research, get_main_positions


def main_position_proportion_by_order():
    main_posisiton_proportions = {}
    latest_date = '2019-06-30'
    for sp in col_stock_profile.find({}):
        shareholders = shareholder_research(sp['_id'])
        if latest_date not in shareholders.main_position_date_list:
            continue
        main_positions = get_main_positions(sp['_id'], datetime.strptime(latest_date, '%Y-%m-%d').date())
        for mp in main_positions:
            if mp.type == '合计':
                main_posisiton_proportions[sp['name']] = mp
    pprint(sorted(main_posisiton_proportions.items(), key=lambda kv: kv[1].proportion, reverse=True))


def top_10_shareholders_proportion_by_order():
    """
    十大股持股比例从高到低排序
    """
    pass
