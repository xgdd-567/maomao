# -*- coding: utf-8 -*-
"""检查 DeepStateMap GeoJSON 数据（只读）。"""
import json
import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = sys.argv[1]
d = json.load(open(path, encoding='utf-8'))
print('id:', d['id'])
print('日期(UTC):', datetime.datetime.utcfromtimestamp(d['id']).isoformat())
fc = d['map']
print('features:', len(fc['features']))
props = {}
for f in fc['features']:
    p = f.get('properties') or {}
    for k, v in p.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            props.setdefault(k, set()).add(str(v))
        else:
            props.setdefault(k, set()).add('<%s>' % type(v).__name__)
for k, v in props.items():
    print('prop', k, '=>', list(v)[:12])
