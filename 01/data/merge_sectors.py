# -*- coding: utf-8 -*-
"""把三个分片（sector-north/donetsk/south）更新的争夺点条目合并回 flashpoints.json（保留 meta 与 news）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MAIN = 'data/flashpoints.json'
WORK = 'data/_work/'

d = json.load(open(MAIN, encoding='utf-8'))
existing = {fp['id']: fp for fp in d['flashpoints']}

merged = []
missing = []
for sector in ['north', 'donetsk', 'south']:
    path = WORK + 'sector-%s.json' % sector
    try:
        items = json.load(open(path, encoding='utf-8'))
    except FileNotFoundError:
        print('MISSING WORK FILE:', path)
        missing.append(sector)
        continue
    for fp in items:
        fid = fp.get('id')
        if fid not in existing:
            print('WARN: unknown id in %s -> %s' % (sector, fid))
            continue
        merged.append(fp)
        existing.pop(fid)
        print('merged %s -> %s' % (sector, fid))

# 未被分片覆盖的条目（保留原样）
for fid, fp in existing.items():
    print('keep original:', fid)
    merged.append(fp)

order = ['sumy-north','kozacha-lopan','velykii-burluk','kupyansk-borova','lyman','sloviansk',
         'kostyantynivka','chasiv-yar','pokrovsk','dobropillya','oleksandrivka-donetsk',
         'huliaipole','stepnohirsk','kharkiv-city','kherson-city','odesa-port','crimea-energy']
merged.sort(key=lambda x: order.index(x['id']) if x['id'] in order else 99)

d['flashpoints'] = merged
with open(MAIN, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('TOTAL flashpoints:', len(merged))
if missing:
    sys.exit(1)
