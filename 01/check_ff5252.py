# -*- coding: utf-8 -*-
"""核验被跳过的 #ff5252 要素（非乌克兰冲突区）是否全部位于乌克兰境外（只读）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

fc = json.load(open('data/control-2026-08-15.geojson', encoding='utf-8'))

# 乌克兰大致边界范围（含克里米亚）：lon 22.1~40.2, lat 44.3~52.4
UA_BBOX = (22.0, 44.2, 40.5, 52.5)

def bbox(geom):
    if geom['type'] == 'Polygon':
        rings = geom['coordinates']
    elif geom['type'] == 'MultiPolygon':
        rings = [r for poly in geom['coordinates'] for r in poly]
    else:
        return None
    xs, ys = [], []
    for ring in rings:
        for p in ring:
            xs.append(p[0]); ys.append(p[1])
    return (min(xs), min(ys), max(xs), max(ys))

print('=== fill=#ff5252 要素 ===')
total = 0
for f in fc['features']:
    p = f.get('properties') or {}
    if p.get('fill') != '#ff5252':
        continue
    total += 1
    b = bbox(f['geometry'])
    name = (p.get('name') or '').split('///')[0].strip()[:50]
    # 判断 bbox 是否与乌克兰 bbox 相交
    overlap = not (b[2] < UA_BBOX[0] or b[0] > UA_BBOX[2] or b[3] < UA_BBOX[1] or b[1] > UA_BBOX[3])
    print('%s | bbox(lon %.2f~%.2f, lat %.2f~%.2f) | 与乌克兰范围相交: %s' % (name, b[0], b[2], b[1], b[3], overlap))
print('总计 #ff5252 要素:', total)
