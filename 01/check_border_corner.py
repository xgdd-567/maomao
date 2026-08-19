# -*- coding: utf-8 -*-
"""检查 ukraine.geojson 边界在德左东南角（lon 29.5~30.2, lat 46.3~47.0）的顶点（只读）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ua = json.load(open('data/ukraine-border.geojson', encoding='utf-8'))
geom = ua['features'][0]['geometry']
rings = geom['coordinates'] if geom['type'] == 'Polygon' else [r for poly in geom['coordinates'] for r in poly]

print('=== 乌克兰边界在德左东南角附近的顶点 ===')
for ring in rings:
    for pt in ring:
        if 29.5 <= pt[0] <= 30.2 and 46.3 <= pt[1] <= 47.0:
            print('lon=%.5f lat=%.5f' % (pt[0], pt[1]))
