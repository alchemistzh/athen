__author__ = 'zh'
# -*- coding: UTF-8 -*-

import xlrd

sz = xlrd.open_workbook(file_contents=open(u'data/sz.xlsx', 'rb').read())
print("Number of worksheets:", sz.nsheets)
print("Worksheet name(s):", sz.sheet_names())
st = sz.sheet_by_index(0)
print(st.name, "rows:", st.nrows, "cols", st.ncols)
for i in range(1, 10):
    row = st.row(i)
    print(row[0].value, row[1].value)
