# -*- coding: utf-8 -*-
"""定位：打印德左多边形落入乌克兰边界多边形内的顶点坐标（只读）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

fc = json.load(open('data/control-2026-08-15.geojson', encoding='utf-8'))
ua = json.load(open('data/ukraine-border.geojson', encoding='utf-8'))

def point_in_ring(pt, ring):
    x, y = pt[0], pt[1]
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y):
            xint = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < xint:
                inside = not inside
        j = i
    return inside

def point_in_poly(pt, geom):
    t = geom['type']
    if t == 'Polygon':
        rings = geom['coordinates']
        if not point_in_ring(pt, rings[0]):
            return False
        for hole in rings[1:]:
            if point_in_ring(pt, hole):
                return False
        return True
    if t == 'MultiPolygon':
        return any(point_in_poly(pt, {'type': 'Polygon', 'coordinates': poly}) for poly in geom['coordinates'])
    return False

ua_geom = ua['features'][0]['geometry']
pmr = None
for f in fc['features']:
    p = f.get('properties') or {}
    if p.get('fill') == '#ff5252' and (p.get('name') or '').startswith('Придністров'):
        pmr = f['geometry']
        break

rings = pmr['coordinates'] if pmr['type'] == 'Polygon' else [r for poly in pmr['coordinates'] for r in poly]
print('=== 落入乌克兰多边形内的德左顶点（前 20 个）===')
shown = 0
for ring in rings:
    for pt in ring:
        if point_in_poly(pt, ua_geom):
            print('lon=%.4f lat=%.4f' % (pt[0], pt[1]))
            shown += 1
            if shown >= 20:
                sys.exit(0)
print('（少于 20 个）')
