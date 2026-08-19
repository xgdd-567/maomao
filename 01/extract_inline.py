# -*- coding: utf-8 -*-
"""把 index.html 中的内联 <script> 块提取为 app.js，并用 <script src="app.js"> 替换。"""
import re

path = 'index.html'
html = open(path, encoding='utf-8').read()

m = re.search(r'<script>\n(.*?)\n</script>', html, re.S)
assert m, '未找到内联脚本块'
code = m.group(1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

html2 = html.replace(m.group(0), '<script src="app.js"></script>')
assert html2 != html
with open(path, 'w', encoding='utf-8') as f:
    f.write(html2)
print('app.js written:', len(code), 'chars; index.html updated')
