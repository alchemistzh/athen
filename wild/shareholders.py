#!/usr/bin/env python3
# coding: utf-8

"""
调用 <东方财富> web 接口获取股票股东情况:
    十大股东
    十大流通股东
    机构持股
    限售解禁

返回数据格式:
    {
        "sdltgd": [ // 十大流通股东
            {
                "rq": "2019-03-31", // 日期
                "sdltgd": [
                    {
                        "rq": "2019-03-31", // 日期
                        "gdmc": "厦门三安电子有限公司", // 股东名称
                        "cgs": "1,213,823,341", // 持股数
                        "zltgbcgbl": "29.76%", // 占流通股本比例
                        "zj": "不变", // 增减
                        "bdbl": "--" // 变动比例
                    },
                ]
            },
        ],
        "sdgd": [ // 十大股东
            {
                "rq": "2019-03-31",
                "sdgd": [
                    {
                        "rq": "2019-03-31", // 日期
                        "gdmc": "厦门三安电子有限公司", // 股东名称
                        "cgs": "1,213,823,341", // 持股数
                        "zltgbcgbl": "29.76%", // 占总股本比例
                        "zj": "不变", // 增减
                        "bdbl": "--" // 变动比例
                    },
                ]
            },
        ],
        "jjcg": [ // 机构持股
            {
                "rq": "2019-06-30",
                "jjcg": [
                    {
                        "jjdm": "163402", // 基金代码
                        "jjmc": "兴全趋势投资混合(LOF)", // 基金名称
                        "cgs": "55,254,308.00", // 持股数
                        "cgsz": "623,268,594.24", // 市值
                        "zzgbb": "1.35%", // 占总股本比
                        "zltb": "1.35%", // 占流通比
                        "zjzb": "3.41%", // 占净值比
                    },
                ]
            },
        ],
        "sdgdcgbd": [ // 十大股东持股变动
            {
                "bdsj": "2019-03-26",
                "mc": "--",
                "gdmc": "福建三安集团有限公司",
                "gflx": "流通A股",
                "cgs": "255,119,092.00",
                "zzgbcgbl": "6.26%",
                "cj": "-19,039,000.00",
                "cjgzygdcgbl": "-6.94%",
                "bdyy": "临时公告"
            },
        ],
        "xsjj": [ // 限售解禁
            {
                "jjsj": "2020-06-01", // 解禁时间
                "jjsl": "5725.74万", // 解禁数量
                "jjgzzgbbl": "5.47%", // 解禁股占总股本比例
                "jjgzltgbbl": "12.04%", // 解禁股占流通股本比例
                "gplx": "定向增发机构配售股份" // 解禁类型
            },
            {
                "jjsj": "2021-07-12",
                "jjsl": "4.99亿",
                "jjgzzgbbl": "47.69%",
                "jjgzltgbbl": "104.98%",
                "gplx": "定向增发机构配售股份"
            }
        ],
        "kggx": { // 控股关系
            "sjkzr": "林秀成", // 实际控制人
            "cgbl": "--" // 持股比例
        }
    }
"""

import requests
from collections import namedtuple
from enum import Enum

from util import parse_percent


headers = {
    "Referer": 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx',
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    "X-Requested-With": 'XMLHttpRequest',
}

shareholder = namedtuple('shareholder', 'name amount proportion change')
fund = namedtuple('fund', 'name code amount value proportion net')
result = namedtuple('get_shareholders_result', 'total float fund restricted')


class Institution(Enum):
    Fund = '基金'
    Insurance = '保险'
    OFII = 'QFII'


def get_shareholders(stock_code):
    """ 获取公司股东情况

    stock_code -- 6位股票代码
    """
    url = 'http://f10.eastmoney.com/ShareholderResearch/ShareholderResearchAjax'
    code = '{}{}'.format('SH' if stock_code.startswith('6') else 'SZ', stock_code)
    resp = requests.get(url, headers=headers, params={'code': code})
    data = resp.json()

    # 十大股东 (按日期分组)
    top_10_total_by_date = []
    for record_by_date in data['sdgd']:
        shareholders = [
            shareholder(
                name=r['gdmc'],
                amount=int(r['cgs'].replace(',', '').strip()),
                proportion=parse_percent(r['zltgbcgbl']),
                change=r['bdbl']
            )
            for r in record_by_date['sdgd']
        ]
        top_10_total_by_date.append({
            'date': record_by_date['rq'],
            'shareholders': shareholders
        })

    # 十大流通股东 (按日期分组)
    top_10_float_by_date = []
    for record_by_date in data['sdltgd']:
        shareholders = [
            shareholder(
                name=r['gdmc'],
                amount=int(r['cgs'].replace(',', '').strip()),
                proportion=parse_percent(r['zltgbcgbl']),
                change=r['bdbl']
            )
            for r in record_by_date['sdltgd']
        ]
        top_10_float_by_date.append({
            'date': record_by_date['rq'],
            'shareholders': shareholders,
        })

    # 基金持股 (按日期分组)
    funds_by_date = []
    for record_by_date in data['jjcg']:
        funds = [
            fund(
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

    from pprint import pprint
    pprint(funds_by_date)

    return result(
        total=top_10_total_by_date,
        float=top_10_float_by_date,
        fund=funds_by_date,
        restricted=[],
    )


get_shareholders('300413')
