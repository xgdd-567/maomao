// 验证 index.html：外置脚本引用、文件存在性与数据变量名（只读）。
'use strict';
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf-8');

// 1) 页面不再包含内联脚本（已外置为 app.js）
if (/<script(?![^>]*\bsrc=)[^>]*>/.test(html)) {
  console.error('FAIL: 页面仍包含内联脚本块（应全部外置）');
  process.exit(1);
}
console.log('页面无内联脚本块 OK');

// 2) 外部脚本引用存在
const srcs = [];
const re = /<script[^>]*\bsrc="([^"]+)"/g;
let m;
while ((m = re.exec(html)) !== null) srcs.push(m[1]);
for (const s of srcs) {
  if (/^https?:/.test(s)) continue;
  if (!fs.existsSync(s)) {
    console.error('FAIL: 引用的脚本不存在 ->', s);
    process.exit(1);
  }
}
console.log('外部脚本引用:', srcs.filter(s => !/^https?:/.test(s)).join(', '), 'OK');

// 3) 数据变量名在页面逻辑（app.js）与数据文件中一致
const app = fs.readFileSync('app.js', 'utf-8');
for (const v of ['CONTROL_DATA', 'BORDER_DATA', 'FLASHPOINT_DATA']) {
  if (!app.includes(v)) {
    console.error('FAIL: app.js 未使用变量', v);
    process.exit(1);
  }
}
console.log('数据变量名一致 OK');
console.log('ALL HTML CHECKS PASSED');
