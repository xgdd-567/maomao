# -*- coding: utf-8 -*-
"""从 DeepStateMap 原始响应中提取控制区 FeatureCollection，并转换乌克兰边界 GeoJSON（只读转换）。"""
import json

# 1) 控制区数据（2026-08-18）
d = json.load(open('deepstate-last.json', encoding='utf-8'))
fc = d['map']
with open('control-2026-08-18.geojson', 'w', encoding='utf-8') as f:
    json.dump(fc, f, ensure_ascii=False)
print('control features:', len(fc['features']))

# 2) 乌克兰国际边界（1991 年边界，含克里米亚）
ua = json.load(open('ukraine.geojson', encoding='utf-8'))
if ua.get('type') != 'FeatureCollection':
    feat = dict(ua)
    feat['properties'] = {'name': 'Ukraine (international border)', 'note': '1991 年国际承认边界'}
    ua = {'type': 'FeatureCollection', 'features': [feat]}
else:
    for feat in ua['features']:
        feat['properties'] = {'name': 'Ukraine (international border)', 'note': '1991 年国际承认边界'}
with open('ukraine-border.geojson', 'w', encoding='utf-8') as f:
    json.dump(ua, f, ensure_ascii=False)
print('border features:', len(ua['features']))
print('done')
