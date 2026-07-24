"""
วางแพลนเที่ยว — Flask trip planner (แบบดูอย่างเดียว)
-----------------------------------
เว็บแอปวางแผนทริปหน้าเดียว: แผนที่ + หมุด + ไทม์ไลน์รายวัน
- ดูได้อย่างเดียว ไม่มีโหมดแก้ไขบนเว็บ แก้ไขทริปได้จากการแก้ DEFAULT_TRIP ในไฟล์นี้เท่านั้น

รันเทสต์ในเครื่อง:
    pip install -r requirements.txt
    python app.py
    เปิด http://localhost:5000

Deploy ดูวิธีได้ใน README.md
"""

import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ---------------------------------------------------------------------------
# ข้อมูลทริป — แก้ตรงนี้แล้ว deploy ใหม่เพื่ออัปเดตแผน
# ---------------------------------------------------------------------------
DEFAULT_TRIP = {
    "name": "ทริปเกาะสมุย <3",
    "days": [
        {
            "id": "d1",
            "label": "วันที่ 1",
            "date": "2026-07-25",
            "places": [
                {
                    "id": "p1",
                    "name": "คอนโด The President สาทร-ราชพฤกษ์ เฟส 3",
                    "lat": 13.7185, "lng": 100.4570,
                    "time": "05:00",
                    "note": "จุดเริ่มต้นเดินทาง",
                    "category": "travel"
                },
                {
                    "id": "p2",
                    "name": "เที่ยวบิน FD 3235 · ดอนเมือง (DMK) → สุราษฎร์ธานี (URT)",
                    "lat": 13.9126, "lng": 100.6068,
                    "time": "07:00",
                    "note": "AirAsia · ถึง 08:15 น. (1 ชม. 15 น.) · ผู้โดยสาร 2 คน",
                    "category": "travel"
                },
                {
                    "id": "p6",
                    "name": "ถึงสนามบินสุราษฎร์ธานี (URT)",
                    "lat": 9.1342, "lng": 99.1354,
                    "time": "08:15",
                    "note": "ลงเครื่องแล้ว",
                    "category": "travel"
                },
                {
                    "id": "p7",
                    "name": "นั่งรถไปท่าเรือดอนสัก",
                    "lat": 9.3167829, "lng": 99.7246064,
                    "time": "10:30",
                    "note": "ใช้เวลาประมาณ 1 ชม. 30 นาที",
                    "category": "travel"
                },
                {
                    "id": "p8",
                    "name": "นั่งเรือไปท่าเรือหน้าทอน เกาะสมุย",
                    "lat": 9.536353, "lng": 99.9331332,
                    "time": "12:00",
                    "note": "เรือเฟอร์รี่ ใช้เวลาประมาณ 1 ชม. 30 นาที",
                    "category": "travel"
                },
                {
                    "id": "p10",
                    "name": "กินข้าวที่ร้านกะปิ สะตอ",
                    "lat": 9.5358252, "lng": 100.0364703,
                    "time": "13:00",
                    "note": "มื้อกลางวัน อาหารใต้",
                    "category": "food"
                },
                {
                    "id": "p11",
                    "name": "เดินเล่นที่เซ็นทรัล สมุย",
                    "lat": 9.5326483, "lng": 100.0618091,
                    "time": "14:30",
                    "note": "เดินเล่น รอเวลาเช็คอิน",
                    "category": "activity"
                },
                {
                    "id": "p3",
                    "name": "เช็คอิน COSI Samui Chaweng Beach",
                    "lat": 9.5311554, "lng": 100.0578517,
                    "time": "15:00",
                    "note": "เกาะสมุย · 1 ห้อง",
                    "category": "travel"
                },
                {
                    "id": "p12",
                    "name": "กินข้าวและดูไฟที่ Coco Tam",
                    "lat": 9.5598146, "lng": 100.0263889,
                    "time": "17:30",
                    "note": "บาร์ริมหาดบ่อผุด มื้อเย็น + ดูไฟโชว์",
                    "category": "food"
                }
            ]
        },
        {
            "id": "d2",
            "label": "วันที่ 2",
            "date": "2026-07-26",
            "places": [
                {
                    "id": "p14",
                    "name": "เดินเล่นหาดเฉวง",
                    "lat": 9.519245, "lng": 100.052729,
                    "time": "07:00",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p15",
                    "name": "จุดชมวิวลาดเกาะ",
                    "lat": 9.4990108, "lng": 100.0574056,
                    "time": "08:00",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p16",
                    "name": "คริสตัล บีช",
                    "lat": 9.4777353, "lng": 100.0670935,
                    "time": "08:30",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p17",
                    "name": "หินตา หินยาย",
                    "lat": 9.4633422, "lng": 100.0361526,
                    "time": "09:00",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p26",
                    "name": "กินข้าวร้านครัวชาวบ้าน",
                    "lat": 9.4555737, "lng": 100.0258679,
                    "time": "10:00",
                    "note": "",
                    "category": "food"
                },
                {
                    "id": "p18",
                    "name": "กินขนมที่ Lolamui Café",
                    "lat": 9.4608005, "lng": 100.0373499,
                    "time": "10:30",
                    "note": "",
                    "category": "food"
                },
                {
                    "id": "p19",
                    "name": "จุดชมวิว Overlap Stone 2",
                    "lat": 9.4631624, "lng": 100.0286327,
                    "time": "11:00",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p20",
                    "name": "กินข้าวที่ร้านหมูชมพู",
                    "lat": 9.472838, "lng": 99.9508295,
                    "time": "12:30",
                    "note": "มื้อกลางวัน",
                    "category": "food"
                },
                {
                    "id": "p21",
                    "name": "หาดลิปะน้อย",
                    "lat": 9.5051365, "lng": 99.9234084,
                    "time": "13:30",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p22",
                    "name": "คาเฟ่ Chill Inn Hostel and Beach Cafe",
                    "lat": 9.4955011, "lng": 99.9229827,
                    "time": "14:00",
                    "note": "",
                    "category": "food"
                },
                {
                    "id": "p23",
                    "name": "กินข้าวมันทะเล ป้าตา เกาะสมุย",
                    "lat": 9.5362255, "lng": 99.932044,
                    "time": "15:00",
                    "note": "",
                    "category": "food"
                },
                {
                    "id": "p24",
                    "name": "กลับโรงแรม COSI Samui Chaweng Beach",
                    "lat": 9.5311554, "lng": 100.0578517,
                    "time": "16:00",
                    "note": "รอเดินเล่นหาดเฉวงตอนเย็น",
                    "category": "travel"
                }
            ]
        },
        {
            "id": "d3",
            "label": "วันที่ 3",
            "date": "2026-07-27",
            "places": [
                {
                    "id": "p27",
                    "name": "กินกาแฟร้าน L.O.T. Samui",
                    "lat": 9.5336627, "lng": 99.9312337,
                    "time": "08:00",
                    "note": "",
                    "category": "food"
                },
                {
                    "id": "p28",
                    "name": "กินร้านอรุณวสวัสดิ์โจ๊ก",
                    "lat": 9.5308611, "lng": 99.933496,
                    "time": "09:00",
                    "note": "",
                    "category": "food"
                },
                {
                    "id": "p29",
                    "name": "น้ำตกหินลาด",
                    "lat": 9.5489448, "lng": 99.8896545,
                    "time": "10:00",
                    "note": "",
                    "category": "activity"
                },
                {
                    "id": "p25",
                    "name": "กินขนมจีนร้านปอเล",
                    "lat": 9.5488573, "lng": 99.9282796,
                    "time": "12:00",
                    "note": "มื้อกลางวัน",
                    "category": "food"
                }
            ]
        },
        {
            "id": "d4",
            "label": "วันที่ 4",
            "date": "2026-07-28",
            "places": [
                {
                    "id": "p4",
                    "name": "เช็คเอาต์ COSI Samui Chaweng Beach",
                    "lat": 9.5311554, "lng": 100.0578517,
                    "time": "12:00",
                    "note": "",
                    "category": "travel"
                },
                {
                    "id": "p5",
                    "name": "เที่ยวบิน DD 575 · สุราษฎร์ธานี (URT) → ดอนเมือง (DMK)",
                    "lat": 9.1342, "lng": 99.1354,
                    "time": "15:20",
                    "note": "Nok Air · ถึง 16:35 น. (1 ชม. 15 น.) · ผู้โดยสาร 2 คน",
                    "category": "travel"
                }
            ]
        }
    ]
}
# category ของแต่ละจุด กำหนดสีหมุด/เลขบนแผนที่และแท็บซ้าย:
#   "food"     = สีแดง   (ร้านอาหาร ร้านกาแฟ คาเฟ่)
#   "activity" = สีเหลือง (กิจกรรม เช่น เดินเล่น ช้อปปิ้ง เที่ยวชม)
#   "travel"   = สีตามวัน (เดินทาง เช็คอิน/เอาต์ หรืออื่นๆ ที่ไม่เข้าสองอย่างข้างบน)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template_string(PAGE_TEMPLATE, trip=DEFAULT_TRIP)


# ---------------------------------------------------------------------------
# HTML / CSS / JS (single-page template)
# ---------------------------------------------------------------------------
PAGE_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{ trip.name }} — วางแพลนเที่ยว</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏝️</text></svg>" />
<meta name="theme-color" content="#4F46E5" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
  :root{
    --bg:#F7F8FA; --surface:#FFFFFF; --surface-2:#F1F3F6;
    --border:#E5E7EB; --text:#0F172A; --text-muted:#64748B;
    --accent:#4F46E5; --accent-soft:#EEF0FF;
    --shadow-sm:0 1px 2px rgba(15,23,42,0.06);
    --shadow-md:0 8px 24px rgba(15,23,42,0.10);
    --radius:14px;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0B0F1A; --surface:#131826; --surface-2:#1B2233;
      --border:#242C3E; --text:#E5E9F2; --text-muted:#8B93A7;
      --accent:#818CF8; --accent-soft:#1E2340;
      --shadow-sm:0 1px 2px rgba(0,0,0,0.35);
      --shadow-md:0 8px 24px rgba(0,0,0,0.5);
    }
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
    color:var(--text); background:var(--bg); -webkit-font-smoothing:antialiased;
  }
  button{font-family:inherit;cursor:pointer;border:none;}

  .trip-header{
    background:var(--surface);color:var(--text);padding:14px 22px;display:flex;align-items:center;gap:12px;
    flex-wrap:wrap;position:sticky;top:0;z-index:500;border-bottom:1px solid var(--border);box-shadow:var(--shadow-sm);
  }
  .trip-title-static{
    font-size:18px;font-weight:800;letter-spacing:-0.01em;max-width:360px;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  }
  .header-spacer{flex:1;}

  .trip-body{display:grid;grid-template-columns:360px 1fr;gap:0;min-height:calc(100vh - 63px);}
  @media (max-width:860px){ .trip-body{grid-template-columns:1fr;} #map{height:360px !important;} }
  .side-panel{background:var(--bg);padding:20px;overflow-y:auto;}
  .day-tabs{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:18px;background:var(--surface-2);padding:5px;border-radius:12px;}
  .day-tab{
    flex:1;min-width:64px;background:transparent;color:var(--text-muted);padding:8px 10px;border-radius:9px;
    font-size:13px;font-weight:600;transition:background .15s ease,color .15s ease;
  }
  .day-tab.active{background:var(--surface);color:var(--text);box-shadow:var(--shadow-sm);}
  .day-label-row{display:flex;align-items:baseline;gap:8px;margin-bottom:14px;}
  .day-label-static{font-size:15px;font-weight:700;color:var(--text);}
  .day-date-static{font-size:12.5px;color:var(--text-muted);}
  .place-list{list-style:none;margin:0;padding:0;}
  .place-item{
    background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
    padding:12px 14px;margin-bottom:10px;box-shadow:var(--shadow-sm);cursor:pointer;
    transition:box-shadow .15s ease, transform .15s ease;
  }
  .place-item:hover{box-shadow:var(--shadow-md);transform:translateY(-1px);}
  .place-item.active{box-shadow:0 0 0 2px var(--accent), var(--shadow-md);}
  .place-top{display:flex;align-items:flex-start;gap:10px;}
  .place-num{
    color:#fff;width:24px;height:24px;border-radius:8px;font-size:12px;font-weight:700;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;
  }
  .place-main{flex:1;min-width:0;}
  .place-name{font-weight:600;font-size:14px;color:var(--text);line-height:1.35;}
  .place-time{font-size:12px;color:var(--accent);font-weight:700;margin-top:2px;}
  .place-note{font-size:12.5px;color:var(--text-muted);margin-top:3px;line-height:1.4;}
  .empty-state{text-align:center;padding:36px 12px;color:var(--text-muted);font-size:13.5px;}

  #map{height:calc(100vh - 63px);width:100%;}
</style>
</head>
<body>
<div id="app"></div>

<script>
  let TRIP = {{ trip | tojson }};

  const PALETTE = ['#4F46E5','#F97316','#10B981','#EC4899','#0EA5E9','#EAB308'];
  const RESTAURANT_COLOR = '#EF4444';
  const ACTIVITY_COLOR = '#EAB308';
  // ปกติแต่ละจุดควรมี "category" ระบุมาจากข้อมูลทริปโดยตรง (food/activity/travel)
  // เผื่อจุดไหนไม่มีค่านี้ ยังเดาจากชื่อได้เป็น fallback
  function guessCategory(p){
    if(/กินข้าว|คาเฟ่/.test(p.name)) return 'food';
    if(/เดินเล่น/.test(p.name)) return 'activity';
    return 'travel';
  }
  function placeColor(p, dayIdx){
    const cat = p.category || guessCategory(p);
    if(cat === 'food') return RESTAURANT_COLOR;
    if(cat === 'activity') return ACTIVITY_COLOR;
    return dayColor(dayIdx);
  }
  const app = document.getElementById('app');

  let state = { trip: TRIP, selectedDayId: TRIP.days[0] ? TRIP.days[0].id : null,
                map: null, markersLayer: null, routeLayer: null, markersById: {} };

  function escapeHtml(s){ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function currentDay(){ return state.trip.days.find(d=>d.id===state.selectedDayId) || state.trip.days[0]; }
  function dayColor(idx){ return PALETTE[((idx%PALETTE.length)+PALETTE.length)%PALETTE.length]; }

  function renderTrip(){
    const trip = state.trip;
    app.innerHTML = `
      <div class="trip-header">
        <div class="trip-title-static">${escapeHtml(trip.name)}</div>
        <div class="header-spacer"></div>
      </div>
      <div class="trip-body">
        <div class="side-panel">
          <div class="day-tabs" id="day-tabs"></div>
          <div class="day-label-row" id="day-field-row"></div>
          <ul class="place-list" id="place-list"></ul>
        </div>
        <div id="map"></div>
      </div>`;

    renderDayTabs(); renderDayFields(); renderPlaceList(); initMapIfNeeded(); updateMapMarkers();
  }

  function renderDayTabs(){
    const wrap = document.getElementById('day-tabs'); const trip = state.trip;
    wrap.innerHTML = trip.days.map(d=>`
      <button class="day-tab ${d.id===state.selectedDayId?'active':''}" data-day="${d.id}">${escapeHtml(d.label)}</button>`).join('');

    wrap.querySelectorAll('.day-tab').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        state.selectedDayId = btn.dataset.day;
        renderDayFields(); renderPlaceList(); updateMapMarkers(); fitMapToDay();
        wrap.querySelectorAll('.day-tab').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
      });
    });
  }

  function renderDayFields(){
    const day = currentDay(); const row = document.getElementById('day-field-row');
    if(!day){ row.innerHTML = ''; return; }
    row.innerHTML = `<div class="day-label-static">${escapeHtml(day.label)}</div>${day.date?`<div class="day-date-static">${escapeHtml(day.date)}</div>`:''}`;
  }

  function renderPlaceList(){
    const list = document.getElementById('place-list'); const day = currentDay();
    if(!day || day.places.length===0){
      list.innerHTML = `<div class="empty-state">ยังไม่มีสถานที่ในวันนี้</div>`;
      return;
    }
    const dayIdx = state.trip.days.indexOf(day);
    list.innerHTML = day.places.map((p,i)=>`
      <li class="place-item" data-place="${p.id}" style="border-left-color:${placeColor(p,dayIdx)}">
        <div class="place-top">
          <div class="place-num" style="background:${placeColor(p,dayIdx)}">${i+1}</div>
          <div class="place-main">
            <div class="place-name">${escapeHtml(p.name)}</div>
            ${p.time?`<div class="place-time">${escapeHtml(p.time)} น.</div>`:''}
            ${p.note?`<div class="place-note">${escapeHtml(p.note)}</div>`:''}
          </div>
        </div>
      </li>`).join('');
    list.querySelectorAll('.place-item').forEach(li=>{
      li.addEventListener('click', ()=> flyToPlace(li.dataset.place));
    });
  }

  function flyToPlace(placeId){
    const day = currentDay(); if(!day || !state.map) return;
    const p = day.places.find(pl=>pl.id===placeId); if(!p) return;
    state.map.flyTo([p.lat,p.lng], Math.max(state.map.getZoom(),15), {duration:0.6});
    const marker = state.markersById[placeId];
    if(marker) marker.openPopup();
    document.querySelectorAll('.place-item').forEach(li=>{
      li.classList.toggle('active', li.dataset.place === placeId);
    });
  }

  function initMapIfNeeded(){
    if(state.map){ state.map.remove(); state.map = null; }
    state.map = L.map('map', {zoomControl:true}).setView([13.7563,100.5018], 11);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      maxZoom:19, subdomains:'abcd',
      attribution:'&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(state.map);
    state.markersLayer = L.layerGroup().addTo(state.map);
    state.routeLayer = L.layerGroup().addTo(state.map);
    addOverviewControl();
    fitMapToDay();
  }

  function addOverviewControl(){
    const OverviewControl = L.Control.extend({
      options:{ position:'topleft' },
      onAdd: function(){
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        const link = L.DomUtil.create('a', '', container);
        link.href = '#';
        link.title = 'ดูภาพรวมทั้งวัน';
        link.style.display = 'flex';
        link.style.alignItems = 'center';
        link.style.justifyContent = 'center';
        link.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg>`;
        L.DomEvent.disableClickPropagation(container);
        L.DomEvent.on(link, 'click', L.DomEvent.stop).on(link, 'click', ()=> fitMapToDay());
        return container;
      }
    });
    new OverviewControl().addTo(state.map);
  }

  function fitMapToDay(){
    if(!state.map) return;
    const day = currentDay();
    if(!day || day.places.length===0) return;
    const bounds = L.latLngBounds(day.places.map(p=>[p.lat,p.lng]));
    state.map.fitBounds(bounds, {padding:[40,40]});
    // don't let the initial view zoom out further than this, even if stops are far apart
    if(state.map.getZoom() < 8) state.map.setZoom(8);
    // and don't zoom in past this just because a day has only one or two close stops
    if(state.map.getZoom() > 15) state.map.setZoom(15);
  }

  function numberIcon(color, num){
    const html = `<div style="background:${color};color:#fff;width:28px;height:28px;border-radius:50%;
      border:2.5px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.28);display:flex;align-items:center;
      justify-content:center;font-family:'Inter',system-ui,sans-serif;font-size:13px;font-weight:700;">${num}</div>`;
    return L.divIcon({className:'', html, iconSize:[28,28], iconAnchor:[14,14]});
  }

  let routeRequestId = 0;
  function isDirectLeg(a,b){
    // เที่ยวบิน = leg starting at a flight pin is the flight itself (not a road)
    // นั่งเรือ = leg arriving at a ferry-ride pin is the sea crossing (routing engines
    // often snap it to the wrong ferry pier, so draw it direct instead)
    return /เที่ยวบิน/.test(a.name) || /นั่งเรือ/.test(b.name);
  }

  const routeCache = {};
  async function fetchRoadRoute(a, b){
    const key = `${a[0]},${a[1]}|${b[0]},${b[1]}`;
    if(routeCache[key]) return routeCache[key];
    try{
      const url = `https://router.project-osrm.org/route/v1/driving/${a[1]},${a[0]};${b[1]},${b[0]}?overview=full&geometries=geojson`;
      const r = await fetch(url);
      const data = await r.json();
      if(data.code === 'Ok' && data.routes && data.routes[0]){
        const path = data.routes[0].geometry.coordinates.map(c=>[c[1],c[0]]);
        routeCache[key] = path;
        return path;
      }
    }catch(e){ /* fall back to straight line below */ }
    return [a, b];
  }

  async function updateMapMarkers(){
    if(!state.map) return;
    const myRequestId = ++routeRequestId;
    state.markersLayer.clearLayers(); state.routeLayer.clearLayers();
    state.markersById = {};
    const day = currentDay(); const dayIdx = day ? state.trip.days.indexOf(day) : 0;
    if(!day) return;

    day.places.forEach((p,i)=>{
      const marker = L.marker([p.lat,p.lng], {icon:numberIcon(placeColor(p,dayIdx),i+1)})
        .bindPopup(`<b>${escapeHtml(p.name)}</b>${p.time?`<br/>${escapeHtml(p.time)} น.`:''}${p.note?`<br/>${escapeHtml(p.note)}`:''}`)
        .addTo(state.markersLayer);
      state.markersById[p.id] = marker;
    });

    const legs = [];
    for(let i=0;i<day.places.length-1;i++){ legs.push([day.places[i], day.places[i+1]]); }
    const paths = await Promise.all(legs.map(([a,b])=>
      isDirectLeg(a,b) ? Promise.resolve([[a.lat,a.lng],[b.lat,b.lng]]) : fetchRoadRoute([a.lat,a.lng],[b.lat,b.lng])
    ));

    if(myRequestId !== routeRequestId) return; // a newer day/refresh started, drop this stale result
    legs.forEach(([a,b], i)=>{
      const dashed = isDirectLeg(a,b);
      const legColor = PALETTE[i % PALETTE.length];
      // white casing underneath each leg so it stays readable over any map background,
      // and each leg gets its own color so consecutive stops are easy to tell apart
      L.polyline(paths[i], {color:'#ffffff', weight: dashed?6:8, opacity:0.9, lineCap:'round'}).addTo(state.routeLayer);
      L.polyline(paths[i], {color:legColor, weight: dashed?3:4.5, opacity:0.95, dashArray: dashed?'6 8':null, lineCap:'round'}).addTo(state.routeLayer);
    });
  }

  renderTrip();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
