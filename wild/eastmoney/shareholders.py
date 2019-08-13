#!/usr/bin/env python3
# coding: utf-8

"""
调用 <东方财富> web 接口获取股票股东情况:
    十大股东
    十大流通股东
    机构持股
    限售解禁

返回数据格式:
    见 samples/shareholders.json
"""

import requests
from collections import namedtuple

from wild.util import parse_percent, str_to_int

# 用于表示 十大股东， 十大流通股东 和 实际控制人
Shareholder = namedtuple('Shareholder', ['name', 'amount', 'proportion', 'change'], defaults=[None]*4)

# 用于表示 基金持股
Fund = namedtuple('Fund', ['name', 'code', 'amount', 'value', 'proportion', 'net'])

# 用于表示 限售解禁
Restricted = namedtuple('Restricted', ['type', 'date', 'amount', 'proportion'])

# 用于表示 query_shareholders 的返回值
Result = namedtuple('query_shareholders_Result', 'total float fund restricted controller main_position_date_list')


def query_shareholders(stock_code):
    """ 获取公司股东情况

    stock_code -- 6 位股票代码
    """
    url = 'http://f10.eastmoney.com/ShareholderResearch/ShareholderResearchAjax'
    headers = {
        "Referer": 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx',
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        "X-Requested-With": 'XMLHttpRequest',
    }
    code = '{}{}'.format('SH' if stock_code.startswith('6') else 'SZ', stock_code)
    resp = requests.get(url, headers=headers, params={'code': code})
    data = resp.json()

    # 十大股东 (按日期分组)
    top_10_total_by_date = []
    for record_by_date in data['sdgd']:
        holders = [
            Shareholder(
                name=r['gdmc'],
                amount=int(r['cgs'].replace(',', '').strip()),
                proportion=parse_percent(r['zltgbcgbl']),
                change=parse_percent(r['bdbl'])
            )
            for r in record_by_date['sdgd']
        ]
        top_10_total_by_date.append({
            'date': record_by_date['rq'],
            'holders': holders
        })

    # 十大流通股东 (按日期分组)
    top_10_float_by_date = []
    for record_by_date in data['sdltgd']:
        holders = [
            Shareholder(
                name=r['gdmc'],
                amount=int(r['cgs'].replace(',', '').strip()),
                proportion=parse_percent(r['zltgbcgbl']),
                change=parse_percent(r['bdbl'])
            )
            for r in record_by_date['sdltgd']
        ]
        top_10_float_by_date.append({
            'date': record_by_date['rq'],
            'holders': holders,
        })

    # 基金持股 (按日期分组)
    funds_by_date = []
    for record_by_date in data['jjcg']:
        funds = [
            Fund(
                code=r['jjdm'],
                name=r['jjmc'],
                amount=int(float(r['cgs'].replace(',', '').strip())),
                value=int(float(r['cgsz'].replace(',', '').strip())),
                proportion=parse_percent(r['zltb']),
                net=parse_percent(r['zjzb']),
            )
            for r in record_by_date['jjcg']
        ]
        funds_by_date.append({
            'date': record_by_date['rq'],
            'funds': funds,
        })

    # 限售解禁
    restricted_ = [
        Restricted(
            date=r['jjsj'],
            type=r['gplx'],
            amount=str_to_int(r['jjsl']),
            proportion=parse_percent(r['jjgzzgbbl']),
        )
        for r in data['xsjj']
    ]

    # 实际控制人
    controller = Shareholder(
        name=data['kggx']['sjkzr'],
        proportion=parse_percent(data['kggx']['cgbl']),
    )

    return Result(
        total=top_10_total_by_date,
        float=top_10_float_by_date,
        fund=funds_by_date,
        restricted=restricted_,
        controller=controller,
        main_position_date_list=data['zlcc_rz']  # 主力持仓日期列表,
    )


if __name__ == '__main__':
    print(query_shareholders('300413'))
