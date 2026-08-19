# -*- coding: utf-8 -*-
"""把 JSON 数据转换为浏览器可用的 JS 变量文件（含 </script 安全转义）。"""
import json

def to_js(var_name, json_path, js_path):
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    body = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    body = body.replace('</', '<\\/')  # 防止 </script> 提前闭合
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('/* 自动生成：' + json_path + ' */\nvar %s = %s;\n' % (var_name, body))
    print(js_path, 'OK', len(body), 'bytes')

to_js('CONTROL_DATA', 'data/control-2026-08-18.geojson', 'data/control.js')
to_js('BORDER_DATA', 'data/ukraine-border.geojson', 'data/border.js')
to_js('FLASHPOINT_DATA', 'data/flashpoints.json', 'data/flashpoints.js')
print('done')
