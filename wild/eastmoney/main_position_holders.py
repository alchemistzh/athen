#!/usr/bin/env python3
# coding: utf-8

"""
调用 <东方财富> web 接口获取股票主力持仓情况 (各类机构的持仓比例)

返回数据格式:
    见 samples/main_position_holders.json
"""

import requests

from enum import Enum


url = 'http://f10.eastmoney.com/ShareholderResearch/MainPositionsHodlerAjax?date=2019-03-31&code=SZ300413'


class Institution(Enum):
    Fund            = '基金'
    Insurance       = '保险'
    OFII            = 'QFII'
    SocialSecurity  = '社保'
    Securities      = '券商'
    Trust           = '信托'
    Other           = '其他'
