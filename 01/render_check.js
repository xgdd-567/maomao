// 渲染逻辑模拟：加载三个数据 JS，复刻 index.html 的分类逻辑并统计（只读）。
'use strict';
const fs = require('fs');
const vm = require('vm');

const ctx = {};
vm.createContext(ctx);
for (const f of ['data/control.js', 'data/border.js', 'data/flashpoints.js']) {
  vm.runInContext(fs.readFileSync(f, 'utf-8'), ctx, { filename: f });
}
const CONTROL = ctx.CONTROL_DATA;
const BORDER = ctx.BORDER_DATA;
const FP = ctx.FLASHPOINT_DATA;

if (!CONTROL || CONTROL.type !== 'FeatureCollection') throw new Error('control.js 数据异常');
if (!BORDER || BORDER.type !== 'FeatureCollection') throw new Error('border.js 数据异常');
if (!FP || !Array.isArray(FP.flashpoints)) throw new Error('flashpoints.js 数据异常');

// 复刻页面分类逻辑
const UKR = { '#01579b': 1, '#0f9d58': 1, '#0288d1': 1 };
const RUS = { '#a52714': 1, '#880e4f': 1 };
const GRAY = { '#bcaaa4': 1, '#bdbdbd': 1 };
let ukr = 0, rus = 0, gray = 0, skipped = 0, points = 0;
for (const f of CONTROL.features) {
  const fill = (f.properties && f.properties.fill) || null;
  const g = f.geometry && f.geometry.type;
  if (g === 'Point') { points++; continue; }
  if (UKR[fill]) ukr++;
  else if (RUS[fill]) rus++;
  else if (GRAY[fill]) gray++;
  else skipped++;
}
console.log('控制区多边形分类: 乌控=%d 俄控=%d 争夺=%d 跳过(非冲突区/无fill)=%d 点位(不渲染)=%d', ukr, rus, gray, skipped, points);

// 边界要素
console.log('边界要素: %d (%s)', BORDER.features.length, BORDER.features[0].geometry.type);

// 争夺点合法性：坐标在乌克兰大致范围（lon 22~41, lat 44~53）
let bad = 0;
for (const fp of FP.flashpoints) {
  if (!(fp.lat >= 44 && fp.lat <= 53 && fp.lon >= 22 && fp.lon <= 41)) {
    console.error('坐标越界:', fp.id, fp.lat, fp.lon);
    bad++;
  }
}
console.log('争夺点: %d 条, 坐标越界: %d', FP.flashpoints.length, bad);
console.log('报道: %d 条', FP.news.length);

// 报道 URL 唯一性
const urls = FP.news.map(n => n.url);
const dup = urls.filter((u, i) => urls.indexOf(u) !== i);
console.log('报道重复 URL: %d', dup.length);

if (bad || dup.length) process.exit(1);
console.log('RENDER SIMULATION OK');
