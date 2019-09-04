#!/usr/bin/env python3
# coding: utf-8

import pymongo
from datetime import date, datetime
from pprint import pprint

from stats.mongodb import col_stock_profile, col_shareholder
from util.datetime import REPORT_DATES
from wild.eastmoney import shareholder_research, get_main_positions


MAX_MARKET_CAPITAL = 100*100000000


def main_position_proportion_by_order():
    main_posisiton_proportions = {}
    for sp in col_stock_profile.find({'market_capital': {'$lt': MAX_MARKET_CAPITAL}}):
        shareholder = col_shareholder.find_one({'_id': sp['_id']})
        if REPORT_DATES[0] not in shareholder['main_position_date_list']:
            continue
        main_positions = get_main_positions(sp['_id'], datetime.strptime(REPORT_DATES[0], '%Y-%m-%d').date())
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


def fund_proportion_by_order(stock_profile_docs):
    """
    基金股持股比例从高到低排序
    """
    stocks_with_fund_proportion = []
    for sp in stock_profile_docs:
        sh = col_shareholder.find_one({'_id': sp['_id']})
        fund = sh.get('fund')
        if not fund or not fund.get(REPORT_DATES[0]):
            continue
        stocks_with_fund_proportion.append({
            'code': sp['_id'],
            'name': sp['name'],
            'proportion': fund[REPORT_DATES[0]]['proportion'],
        })
    ordered = sorted(stocks_with_fund_proportion, key=lambda k: k['proportion'], reverse=True)
    for i in ordered:
        print(i['code'], i['name'], round(i['proportion'], 2))


if __name__ == '__main__':
    fund_proportion_by_order(col_stock_profile.find({'market_capital': {'$lt': MAX_MARKET_CAPITAL}}))
