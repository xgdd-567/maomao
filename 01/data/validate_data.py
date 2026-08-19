# -*- coding: utf-8 -*-
"""验证数据文件 JSON 语法与关键字段（只读）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

files = ['data/control-2026-08-18.geojson', 'data/ukraine-border.geojson', 'data/flashpoints.json', 'data/towns_geo.json']
for path in files:
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    if path.endswith('control-2026-08-18.geojson'):
        assert d['type'] == 'FeatureCollection'
        fills = {}
        for feat in d['features']:
            f_ = (feat.get('properties') or {}).get('fill')
            fills[f_] = fills.get(f_, 0) + 1
        print(path, 'OK features=%d fills=%s' % (len(d['features']), {k: v for k, v in fills.items()}))
    elif path.endswith('ukraine-border.geojson'):
        print(path, 'OK type=%s features=%d' % (d['type'], len(d['features'])))
    elif path.endswith('flashpoints.json'):
        fps = d['flashpoints']
        assert len(fps) == 18, 'flashpoints=%d' % len(fps)
        for fp in fps:
            assert 'name' in fp and 'lat' in fp and 'lon' in fp and 'summary' in fp and 'reports' in fp, fp.get('id')
            for r in fp['reports']:
                assert r['url'].startswith('https://'), (fp['id'], r)
        news = d['news']
        for n in news:
            assert n['url'].startswith('https://'), n
        print(path, 'OK flashpoints=%d news=%d' % (len(fps), len(news)))
    else:
        print(path, 'OK towns=%d' % len(d))
print('ALL JSON VALID')
