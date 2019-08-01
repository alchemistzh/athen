
import requests

url = 'http://query.sse.com.cn/security/stock/getStockListData.do'

headers = {
    'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

params = {
    'isPagination': 'true',
    'stockCode': '',
    'csrcCode': '',
    'areaName': '',
    'stockType': 1,
    'pageHelp.cacheSize': 1,
    'pageHelp.beginPage': 31,
    'pageHelp.pageSize': 50,
    'pageHelp.pageNo': 2,
}

resp = requests.get(url, headers=headers, params=params)
if resp.ok:
    print(resp.json())
