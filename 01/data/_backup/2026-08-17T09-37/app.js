(function () {
  'use strict';

  /* ============ 工具 ============ */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* ============ 地图初始化 ============ */
  var map = L.map('map', { zoomControl: true, attributionControl: true })
    .setView([49.2, 31.8], 6);

  var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });
  var esriStreet = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: '&copy; Esri, HERE, Garmin, FAO, NOAA, USGS'
  });
  var esri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: '&copy; Esri, Maxar, Earthstar Geographics'
  });
  esriStreet.addTo(map);

  /* ============ 图层样式映射 ============ */
  // DeepStateMap 原始 fill 色 → 分类
  var UKR_FILLS = { '#01579b': 1, '#0f9d58': 1, '#0288d1': 1 };  // 乌克兰控制（解放；#0288d1 = 新增「Liberated」类）
  var RUS_FILLS = { '#a52714': 1, '#880e4f': 1 };        // 俄罗斯控制（2022 后 / 2014 前占领）
  var GRAY_FILLS = { '#bcaaa4': 1, '#bdbdbd': 1 };       // 争夺 / 状态不明
  // #ff5252 为德左、加里宁格勒等非乌克兰冲突区，跳过

  function layerFor(fill) {
    if (UKR_FILLS[fill]) return 'ukr';
    if (RUS_FILLS[fill]) return 'rus';
    if (GRAY_FILLS[fill]) return 'gray';
    return null;
  }

  var STYLE = {
    ukr:  { color: '#1565c0', weight: 1.2, fillColor: '#1976d2', fillOpacity: 0.42 },
    rus:  { color: '#b71c1c', weight: 1.2, fillColor: '#d32f2f', fillOpacity: 0.45 },
    gray: { color: '#e65100', weight: 1.4, fillColor: '#f9a825', fillOpacity: 0.5, dashArray: '4 3' }
  };

  var ukrLayer = L.geoJSON(null, { style: STYLE.ukr });
  var rusLayer = L.geoJSON(null, { style: STYLE.rus });
  var grayLayer = L.geoJSON(null, { style: STYLE.gray });

  CONTROL_DATA.features.forEach(function (f) {
    var fill = (f.properties && f.properties.fill) || null;
    var cls = layerFor(fill);
    if (!cls) return;
    var target = cls === 'ukr' ? ukrLayer : (cls === 'rus' ? rusLayer : grayLayer);
    target.addData(f);
  });
  ukrLayer.addTo(map);
  rusLayer.addTo(map);
  grayLayer.addTo(map);

  /* ============ 原疆域边界线 ============ */
  var borderLayer = L.geoJSON(BORDER_DATA, {
    style: { color: '#ffd54f', weight: 2.6, dashArray: '8 6', fill: false, opacity: 0.95 },
    interactive: false
  }).addTo(map);

  /* ============ 争夺点标记 ============ */
  var flashLayer = L.layerGroup();
  var markers = {};

  function popupHtml(fp) {
    var h = '<div class="pop">';
    h += '<h4>' + esc(fp.name) + '</h4>';
    h += '<div class="meta">' + esc(fp.sector) + ' · ' + esc(fp.timeline) + '<br>' + esc(fp.nameEn) + '</div>';
    h += '<div class="status ' + esc(fp.type) + '">' +
         (fp.type === 'contested' ? '⚔ 争夺中 / 双方交火' : '◆ 打击/袭击焦点') +
         ' —— ' + esc(fp.status) + '</div>';
    h += '<p>' + esc(fp.summary) + '</p>';
    h += '<div style="font-weight:700;margin-bottom:3px;">相关报道：</div><ul>';
    fp.reports.forEach(function (r) {
      h += '<li><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' +
           esc(r.title) + '</a> <span style="color:#888">(' + esc(r.date) + ')</span></li>';
    });
    h += '</ul></div>';
    return h;
  }

  FLASHPOINT_DATA.flashpoints.forEach(function (fp) {
    var icon = L.divIcon({
      className: '',
      html: '<div style="width:14px;height:14px;border-radius:50%;background:' +
            (fp.type === 'contested' ? '#ef6c00' : '#7b1fa2') +
            ';border:2px solid #fff;box-shadow:0 0 0 2px ' +
            (fp.type === 'contested' ? '#b71c1c' : '#4a148c') + ',0 1px 4px rgba(0,0,0,.5);"></div>',
      iconSize: [14, 14], iconAnchor: [7, 7]
    });
    var m = L.marker([fp.lat, fp.lon], { icon: icon })
      .bindPopup(popupHtml(fp), { maxWidth: 360 });
    markers[fp.id] = m;
    flashLayer.addLayer(m);
  });
  flashLayer.addTo(map);

  /* ============ 图层控制 ============ */
  var baseMaps = { '街道图 (Esri)': esriStreet, '卫星图 (Esri)': esri, '街道图 (OSM，备用)': osm };
  var overlayMaps = {
    '原疆域边界（1991 年）': borderLayer,
    '乌克兰控制区': ukrLayer,
    '俄罗斯控制区': rusLayer,
    '争夺区/状态不明': grayLayer,
    '争夺点与焦点（近一月）': flashLayer
  };
  L.control.layers(baseMaps, overlayMaps, { collapsed: false }).addTo(map);

  /* ============ 右侧面板 ============ */
  var listEl = document.getElementById('list');
  var tabFp = document.querySelector('[data-tab=fp]');
  var tabNews = document.querySelector('[data-tab=news]');
  document.getElementById('cntFp').textContent = FLASHPOINT_DATA.flashpoints.length;
  document.getElementById('cntNews').textContent = FLASHPOINT_DATA.news.length;

  function renderFlashpoints() {
    var html = '';
    FLASHPOINT_DATA.flashpoints.forEach(function (fp) {
      var tag = fp.type === 'contested' ? '<span class="tag contested">争夺</span>'
                                        : '<span class="tag strike">打击焦点</span>';
      html += '<div class="item" data-id="' + esc(fp.id) + '">' +
              '<div class="t">' + esc(fp.name) + '</div>' +
              '<div class="m">' + tag + '<span>' + esc(fp.sector) + '</span>' +
              '<span>' + esc(fp.timeline) + '</span></div></div>';
    });
    listEl.innerHTML = html || '<div class="empty">暂无数据</div>';
    listEl.querySelectorAll('.item').forEach(function (el) {
      el.addEventListener('click', function () {
        var fp = FLASHPOINT_DATA.flashpoints.find(function (x) { return x.id === el.dataset.id; });
        if (!fp) return;
        var m = markers[fp.id];
        map.flyTo([fp.lat, fp.lon], Math.max(map.getZoom(), 9), { duration: 0.8 });
        setTimeout(function () { m.openPopup(); }, 850);
      });
    });
  }

  function renderNews() {
    var html = '';
    FLASHPOINT_DATA.news.forEach(function (n) {
      html += '<div class="item" style="cursor:default">' +
              '<div class="t"><a href="' + esc(n.url) + '" target="_blank" rel="noopener">' + esc(n.title) + '</a></div>' +
              '<div class="m"><span class="tag news-src">' + esc(n.source) + '</span>' +
              '<span>' + esc(n.date) + '</span></div></div>';
    });
    listEl.innerHTML = html || '<div class="empty">暂无数据</div>';
  }

  tabFp.addEventListener('click', function () {
    tabFp.classList.add('active'); tabNews.classList.remove('active');
    renderFlashpoints();
  });
  tabNews.addEventListener('click', function () {
    tabNews.classList.add('active'); tabFp.classList.remove('active');
    renderNews();
  });
  renderFlashpoints();

  /* ============ 底部说明展开 ============ */
  var footEl = document.getElementById('footer');
  var footCollapsed = footEl.innerHTML;
  var expanded = false;
  function bindToggleFoot() {
    document.getElementById('toggleFoot').addEventListener('click', function () {
      if (!expanded) {
        footEl.innerHTML = '<b>详细说明：</b>' +
          '1)「原疆域」为乌克兰 1991 年国际承认边界（含克里米亚），数据为 OSM/Natural Earth 派生，属示意精度。<br>' +
          '2)「实际控制区」分为乌控（蓝）与俄控（红）两类，多边形来自 DeepStateMap.live 公开 API（2026-08-14 16:06 UTC 快照）。俄控含 2014 年占领的克里米亚与顿巴斯部分区域（该数据源以深色区分）。<br>' +
          '3)「争夺区」= DeepState 标注为「状态不明（Статус невідомий）」的地带，多为双方接触线附近的灰色地带，不代表精确前线。<br>' +
          '4) 争夺点与战况摘要逐条摘自 ISW 2026-08-08 / 08-09 / 08-10 / 08-11 / 08-12 / 08-13 / 08-14 七份评估报告原文（标题栏已列链接），报道链接均为报告中引用的真实公开来源（Reuters、Bloomberg、FT、Suspilne、Militarnyi 等）。<br>' +
          '5) 战线每天变动，本图控制线为 2026-08-14 快照；ISW 对俄方 2026 年 7 月下旬在苏梅/哈尔科夫北部的进展声称持「缺乏证据」评估。' +
          '<br><span class="more" id="toggleFoot2">收起</span>';
        document.getElementById('toggleFoot2').addEventListener('click', function () {
          footEl.innerHTML = footCollapsed;
          expanded = false;
          bindToggleFoot();
        });
        expanded = true;
      }
    });
  }
  bindToggleFoot();
})();