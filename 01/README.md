# 俄乌冲突战况地图（网页版）

制作日期：2026-08-19 · 覆盖时段：**2026-08-16 ~ 2026-08-19（最近三天）**

## 使用方法

**方式一（推荐）**：直接双击打开 `index.html`（数据已内联为本地 JS 文件，无需服务器；需联网加载 Leaflet 与底图瓦片）。

**方式二（本地服务器）**：

```
python -m http.server 8765
# 浏览器打开 http://127.0.0.1:8765/
```

## 页面内容

| 图层 | 颜色 | 含义 |
|---|---|---|
| 原疆域 | 黄色虚线 | 乌克兰 1991 年国际承认边界（含克里米亚，示意精度） |
| 乌克兰控制区 | 蓝色 | 实际控制（2026-08-18 快照） |
| 俄罗斯控制区 | 红色 | 实际控制，含 2014 年占领的克里米亚与顿巴斯部分区域 |
| 争夺区 | 琥珀色斜线 | 控制状态不明（灰色地带） |
| 争夺点（橙圆）/ 打击焦点（紫圆） | — | 最近三天 18 个焦点，点击弹窗查看战况摘要与报道链接 |

右侧面板：「争夺点」列表（点击地图聚焦）+「相关报道」10 条（近三天，新窗口打开）。

## 数据来源（全部真实公开来源，非虚构）

- **控制区多边形**：DeepStateMap.live 公开 API 快照（2026-08-18 14:50），乌克兰开源情报项目，**立场亲乌**，未核实为官方数据；其「状态不明」地带在本图标注为「争夺区」。
- **战况与争夺点**：ISW（美国战争研究所）《Russian Offensive Campaign Assessment》——
  - [2026-08-17](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-august-17-2026/)（覆盖 8/16-17 战况）
  - [官方控制评估图 2026-08-18](https://understandingwar.org/map/assessed-control-of-terrain-in-the-russo-ukrainian-war-august-18-2026-at-130-pm-et/)
- **报道链接**：仅保留近三天（2026-08-16 ~ 08-19）的真实公开来源（Reuters/AP、BBC、Kyiv Independent、Suspilne、Ukrainska Pravda、CNBC、Al Jazeera 等）。
- **边界**：OSM/Natural Earth 派生（[countriesgeojson](https://github.com/glynnbird/countriesgeojson)）。
- **城镇坐标**：Photon（OpenStreetMap 地理编码）验证。

> 重要声明：战线每日变动，本图控制区为 2026-08-18 快照；ISW 评估 8 月 17 日俄乌双方均无确认推进，其对俄方在亚历山德里夫卡/胡里艾伯莱方向的大规模推进声称（含大量 AI 篡改视频）持续持「不可信」评估。本页为个人整理的信息可视化，非官方地图。

## 文件结构

```
index.html          主页面
app.js              地图逻辑（Leaflet）
data/
  control.js        控制区数据（DeepStateMap 2026-08-18，525 要素）
  border.js         乌克兰国际边界
  flashpoints.js    争夺点（18）+ 报道（10，近三天）
  _raw/             原始下载资料（ISW 报告 HTML/文本、DeepState 原始 JSON 等，可审计）
  *.py / *.js       数据提取与验证脚本
verify_html.js      页面引用完整性检查（node verify_html.js）
render_check.js     渲染逻辑模拟（node render_check.js）
```

## 重新生成 / 更新数据

1. 更新 `data/_raw/deepstate-last.json`（`curl https://deepstatemap.live/api/history/last`）并复制为 `data/deepstate-last.json`
2. 更新 `data/prep_geojson.py`、`data/convert_js.py`、`data/validate_data.py` 中的快照日期文件名，运行 `python data/prep_geojson.py && python data/convert_js.py`（注意：`prep_geojson.py` 在 `data/` 目录下运行，`convert_js.py` 在项目根目录运行）
3. 更新 `data/flashpoints.json` 中的战况与报道（基于新的 ISW 报告；可按战线分片更新到 `data/_work/sector-*.json` 后用 `python data/merge_sectors.py` 合并）
4. 运行 `python data/validate_data.py && node --check data/*.js && node verify_html.js && node render_check.js`
