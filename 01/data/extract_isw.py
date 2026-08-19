# -*- coding: utf-8 -*-
"""从 ISW 报告 HTML 中提取正文纯文本，用于人工核对战况细节（只读解析，不修改数据）。"""
import re
import html as htmlmod
import sys

src = sys.argv[1]
dst = sys.argv[2]

raw = open(src, encoding='utf-8').read()
m = re.search(r'<article[^>]*>(.*?)</article>', raw, re.S)
body = m.group(1) if m else raw
text = re.sub(r'<script.*?</script>', ' ', body, flags=re.S)
text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
text = re.sub(r'<[^>]+>', '\n', text)
text = htmlmod.unescape(text)
lines = [l.strip() for l in text.split('\n') if l.strip()]
out = '\n'.join(lines)
with open(dst, 'w', encoding='utf-8') as f:
    f.write(out)
print('chars:', len(out))
