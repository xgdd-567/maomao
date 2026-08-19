# -*- coding: utf-8 -*-
"""分析 DeepStateMap 数据：按 fill 颜色统计多边形与名称（只读）。"""
import json
import sys
import io
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open(sys.argv[1], encoding='utf-8'))
fc = d['map']

by_fill = {}
for f in fc['features']:
    p = f.get('properties') or {}
    fill = p.get('fill', '(none)')
    geo = f.get('geometry') or {}
    by_fill.setdefault(fill, []).append((p.get('name', ''), geo.get('type')))

for fill, items in sorted(by_fill.items()):
    polys = sum(1 for _, t in items if t in ('Polygon', 'MultiPolygon'))
    lines = sum(1 for _, t in items if t in ('LineString', 'MultiLineString'))
    pts = sum(1 for _, t in items if t == 'Point')
    print('fill=%s  total=%d  poly=%d line=%d pt=%d' % (fill, len(items), polys, lines, pts))
    names = [n.split('///')[0].strip()[:40] for n, t in items if t in ('Polygon', 'MultiPolygon')]
    print('   多边形名称样例:', names[:6])
