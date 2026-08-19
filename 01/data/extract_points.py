# -*- coding: utf-8 -*-
"""提取 DeepState 数据中的 Point 要素（城镇/设施），输出名称+坐标（只读）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open(sys.argv[1], encoding='utf-8'))
fc = d['map']

for f in fc['features']:
    geo = f.get('geometry') or {}
    if geo.get('type') != 'Point':
        continue
    p = f.get('properties') or {}
    name = (p.get('name') or '').split('///')[0].strip()
    coords = geo['coordinates']
    print('%s\t%.5f\t%.5f' % (name[:60], coords[0], coords[1]))
