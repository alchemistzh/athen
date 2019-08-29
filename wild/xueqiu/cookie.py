#!/usr/bin/env python3
# coding: utf-8


def get_cookies(session):
    """
    访问雪球首页, 获取 cookie
    """
    url = 'https://xueqiu.com'
    headers = {
        'Accept': '*/*',
        'Host': 'xueqiu.com',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }
    resp = session.get(url, headers=headers)
    return resp.cookies
