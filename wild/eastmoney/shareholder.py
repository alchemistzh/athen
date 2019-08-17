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
Shareholder = namedtuple('Shareholder', [
    'name',           # 股东名称
    'amount',         # 持股数量
    'proportion',     # 持股占流通股比例
    'change',         # 持股变化状态 ("不变", "新进", 或增减数量, 如 "222万")
    'change_percent'  # 持股变化比例
], defaults=[None]*5)

# 用于表示 基金持股
Fund = namedtuple('Fund', [
    'name',        # 基金名称
    'code',        # 基金代码
    'amount',      # 持股数量
    'value',       # 持股市值
    'proportion',  # 占流通股比例
    'net'          # 占基金净值比例
])

# 用于表示 限售解禁
Restricted = namedtuple('Restricted', [
    'type',       # 解禁类型
    'date',       # 解禁时间
    'amount',     # 解禁数量
    'proportion'  # 解禁股占总股本比例
])

# 用于表示截止某一日期的股东情况
# ShareholderResearch = namedtuple('ShareholderResearch', [
#     'total',                   # 十大股东
#     'float',                   # 十大流通股东
#     'fund',                    # 基金持股
#     'restricted',              # 限售解禁
#     'controller',              # 实际控制人
#     'main_position_date_list'  # 主力持仓日期列表
# ], defaults=[None]*6)


def shareholder_research(stock_code):
    """ 股东研究

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

    result = {}

    # 十大股东
    for sdgd in data['sdgd']:
        shareholders = [
            Shareholder(
                name=i['gdmc'],
                amount=int(i['cgs'].replace(',', '').strip()),
                proportion=parse_percent(i['zltgbcgbl']),
                change=i['zj'],
                change_percent=parse_percent(i['bdbl'])
            )
            for i in sdgd['sdgd']
        ]
        result.setdefault(sdgd['rq'], {})['total'] = shareholders

    # 十大流通股东
    for sdltgd in data['sdltgd']:
        shareholders = [
            Shareholder(
                name=i['gdmc'],
                amount=int(i['cgs'].replace(',', '').strip()),
                proportion=parse_percent(i['zltgbcgbl']),
                change=i['zj'],
                change_percent=parse_percent(i['bdbl'])
            )
            for i in sdltgd['sdltgd']
        ]
        result.setdefault(sdltgd['rq'], {})['float'] = shareholders

    # 基金持股
    for jjcg in data['jjcg']:
        funds = [
            Fund(
                code=i['jjdm'],
                name=i['jjmc'],
                amount=int(float(i['cgs'].replace(',', '').strip())),
                value=int(float(i['cgsz'].replace(',', '').strip())),
                proportion=parse_percent(i['zltb']),
                net=parse_percent(i['zjzb']),
            )
            for i in jjcg['jjcg']
        ]
        result.setdefault(jjcg['rq'], {})['funds'] = funds

    # 限售解禁
    result['restricted'] = [
        Restricted(
            date=i['jjsj'],
            type=i['gplx'],
            amount=str_to_int(i['jjsl']),
            proportion=parse_percent(i['jjgzzgbbl']),
        )
        for i in data['xsjj']
    ]

    # 实际控制人
    result['controller'] = Shareholder(
        name=data['kggx']['sjkzr'],
        proportion=parse_percent(data['kggx']['cgbl']),
    )

    # 主力持仓日期列表
    result['main_position_date_list']=data['zlcc_rz']

    return result


if __name__ == '__main__':
    sr = shareholder_research('300753')
    from pprint import pprint
    pprint(sr['2019-06-30']['float'])
    pprint(sr['2019-06-30']['funds'])
