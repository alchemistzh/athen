__author__ = 'zh'
# -*- coding: UTF-8 -*-

import xlrd
import os

print(os.getcwd())

book = xlrd.open_workbook(file_contents=open(u'excel/test.xls', 'rb').read())
print("The number of worksheets is", book.nsheets)
print("Worksheet name(s):", book.sheet_names())
sh = book.sheet_by_index(0)
print(sh.name, sh.nrows, sh.ncols)
for rx in range(1, sh.nrows):
    row = sh.row(rx)
    if row[1].value != u'\u5df2\u5904\u7406':  # 已处理
        print(rx, row[0].value)
