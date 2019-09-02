#!/usr/bin/env python3
# coding: utf-8

import pymongo
from datetime import date, datetime
from pprint import pprint

from .mongodb import col_stock_profile, col_shareholder
from wild.eastmoney import shareholder_research, get_main_positions


LATEST_DATE = '2019-06-30'
MAX_MARKET_CAPITAL = 100*100000000


def main_position_proportion_by_order():
    main_posisiton_proportions = {}
    for sp in col_stock_profile.find({'market_capital': {'$lt': MAX_MARKET_CAPITAL}}):
        shareholder = col_shareholder.find_one({'_id': sp['_id']})
        if LATEST_DATE not in shareholder['main_position_date_list']:
            continue
        main_positions = get_main_positions(sp['_id'], datetime.strptime(LATEST_DATE, '%Y-%m-%d').date())
        for mp in main_positions:
            if mp.type == '合计':
                main_posisiton_proportions[sp['name']] = mp
    by_order = sorted(main_posisiton_proportions.items(), key=lambda kv: kv[1].proportion, reverse=True)
    for name, mp in by_order:
        print(name, mp.proportion)


def top_10_shareholders_proportion_by_order():
    """
    十大股持股比例从高到低排序
    """
    pass


if __name__ == '__main__':
    main_position_proportion_by_order()
