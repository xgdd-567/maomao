# -*- coding: utf-8 -*-
"""用 Photon (OpenStreetMap) 批量地理编码城镇坐标，输出 JSON（只读查询）。"""
import json
import sys
import io
import time
import urllib.request
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# (查询名, 显示名, 地区限定)
TOWNS = [
    ("Kozacha Lopan", "科扎恰洛潘 Kozacha Lopan", "Kharkiv"),
    ("Velykyi Burluk", "大布尔卢克 Velykyi Burluk", "Kharkiv"),
    ("Artilne", "阿尔蒂尔内 Artilne", "Kharkiv"),
    ("Kupyansk", "库皮扬斯克 Kupyansk", "Kharkiv"),
    ("Borova", "博罗瓦 Borova", "Kharkiv"),
    ("Lyman", "莱曼 Lyman", "Donetsk"),
    ("Slovyansk", "斯拉维扬斯克 Slovyansk", "Donetsk"),
    ("Kostyantynivka", "康斯坦丁尼夫卡 Kostyantynivka", "Donetsk"),
    ("Chasiv Yar", "恰西夫亚尔 Chasiv Yar", "Donetsk"),
    ("Pokrovsk", "波克罗夫斯克 Pokrovsk", "Donetsk"),
    ("Bilytske", "比利茨凯 Bilytske", "Donetsk"),
    ("Dobropillya", "多布罗皮利亚 Dobropillya", "Donetsk"),
    ("Oleksandrivka", "亚历山德里夫卡 Oleksandrivka", "Donetsk"),
    ("Hulyaipole", "胡里艾伯莱 Hulyaipole", "Zaporizhzhia"),
    ("Stepnohirsk", "斯捷普诺希尔斯克 Stepnohirsk", "Zaporizhzhia"),
    ("Zaporizhzhia", "扎波罗热 Zaporizhzhia", "Zaporizhzhia"),
    ("Odesa", "敖德萨 Odesa", "Odesa"),
    ("Kherson", "赫尔松 Kherson", "Kherson"),
    ("Sumy", "苏梅 Sumy", "Sumy"),
    ("Mohrytsya", "莫赫里察 Mohrytsya", "Sumy"),
    ("Kindrativka", "金德拉蒂夫卡 Kindrativka", "Sumy"),
    ("Ivolzhanske", "伊沃尔然斯克 Ivolzhanske", "Sumy"),
    ("Nova Sich", "新西奇 Nova Sich", "Sumy"),
    ("Toretsk", "托列茨克 Toretsk", "Donetsk"),
    ("Druzhkivka", "德鲁日基夫卡 Druzhkivka", "Donetsk"),
    ("Novohrodivka", "新赫罗迪夫卡 Novohrodivka", "Donetsk"),
    ("Siversk", "西维尔斯克 Siversk", "Donetsk"),
    ("Vuhledar", "武赫莱达尔 Vuhledar", "Donetsk"),
    ("Kurakhove", "库拉霍韦 Kurakhove", "Donetsk"),
    ("Velyka Novosilka", "大诺沃西尔卡 Velyka Novosilka", "Donetsk"),
    ("Kramatorsk", "克拉马托尔斯克 Kramatorsk", "Donetsk"),
    ("Kharkiv", "哈尔科夫 Kharkiv", "Kharkiv"),
]

def geocode(q, region):
    params = urllib.parse.urlencode({"q": q + " " + region, "limit": 3})
    url = "https://photon.komoot.io/api/?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "war-map-builder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    for f in data.get("features", []):
        props = f.get("properties", {})
        if props.get("countrycode") == "UA" or (props.get("country") or "").lower().find("ukrain") >= 0:
            lon, lat = f["geometry"]["coordinates"]
            return {"lon": round(lon, 5), "lat": round(lat, 5),
                    "name": props.get("name"), "osm_type": props.get("osm_type"), "osm_id": props.get("osm_id")}
    return None

out = {}
for q, display, region in TOWNS:
    try:
        res = geocode(q, region)
        out[q] = {"display": display, "geo": res}
        print(q, "=>", res)
    except Exception as e:
        out[q] = {"display": display, "geo": None, "error": str(e)}
        print(q, "=> ERROR", e)
    time.sleep(0.6)

with open("towns_geo.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved towns_geo.json")
