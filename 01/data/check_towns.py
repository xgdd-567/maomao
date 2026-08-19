# -*- coding: utf-8 -*-
"""点-多边形检查：判断城镇落在 DeepState 控制区数据的哪个类别（只读）。"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open('deepstate-last.json', encoding='utf-8'))
fc = d['map']

FILL_CLASS = {
    '#01579b': '乌控(解放)',
    '#0f9d58': '乌控(解放)',
    '#a52714': '俄控(2022后占领)',
    '#880e4f': '俄控(2014前占领)',
    '#bcaaa4': '争夺/状态不明',
    '#bdbdbd': '争夺/状态不明',
    '#ff5252': '非乌克兰冲突区',
}

def point_in_ring(pt, ring):
    x, y = pt
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

def point_in_geom(pt, geom):
    t = geom['type']
    if t == 'Polygon':
        rings = geom['coordinates']
        outer = rings[0]
        if not point_in_ring(pt, outer):
            return False
        for hole in rings[1:]:
            if point_in_ring(pt, hole):
                return False
        return True
    if t == 'MultiPolygon':
        for poly in geom['coordinates']:
            if point_in_geom(pt, {'type': 'Polygon', 'coordinates': poly}):
                return True
    return False

# (显示名, lon, lat)
TOWNS = [
    ('Lyman 莱曼', 37.8168, 48.9801),
    ('Kostyantynivka 康斯坦丁尼夫卡', 37.6924, 48.5349),
    ('Pokrovsk 波克罗夫斯克', 37.1773, 48.2771),
    ('Kupyansk 库皮扬斯克', 37.61, 49.75),
    ('Kozacha Lopan 科扎恰洛潘', 36.1921, 50.3296),
    ('Hulyaipole 胡里艾伯莱', 36.2657, 47.6655),
    ('Vuhledar 武赫莱达尔', 37.2461, 47.7810),
    ('Odesa 敖德萨', 30.7323, 46.4843),
    ('Kherson 赫尔松', 32.61, 46.64),
    ('Sumy 苏梅', 34.80, 50.91),
    ('Zaporizhzhia 扎波罗热', 35.1183, 47.8508),
    ('Chasiv Yar 恰西夫亚尔', 37.8373, 48.5874),
    ('Toretsk 托列茨克', 37.8501, 48.3971),
    ('Slovyansk 斯拉维扬斯克', 37.6012, 48.8482),
    ('Borova 博罗瓦', 37.6253, 49.3800),
    ('Siversk 西维尔斯克', 38.0902, 48.8676),
    ('Novohrodivka 新赫罗迪夫卡', 37.3400, 48.1997),
    ('Druzhkivka 德鲁日基夫卡', 37.5250, 48.6199),
    ('Kurakhove 库拉霍韦', 37.2826, 47.9835),
    ('Velyka Novosilka 大诺沃西尔卡', 36.8397, 47.8437),
    ('Kramatorsk 克拉马托尔斯克', 37.5844, 48.7389),
    ('Kharkiv 哈尔科夫', 36.2310, 49.9923),
]

for name, lon, lat in TOWNS:
    hits = []
    for f in fc['features']:
        fill = (f.get('properties') or {}).get('fill')
        if fill not in FILL_CLASS:
            continue
        if point_in_geom((lon, lat), f['geometry']):
            hits.append(FILL_CLASS[fill])
    print('%s -> %s' % (name, hits if hits else '（无覆盖/边界外）'))
