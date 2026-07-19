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
                    "note": "จุดเริ่มต้นเดินทาง"
                },
                {
                    "id": "p2",
                    "name": "เที่ยวบิน FD 3235 · ดอนเมือง (DMK) → สุราษฎร์ธานี (URT)",
                    "lat": 13.9126, "lng": 100.6068,
                    "time": "07:00",
                    "note": "AirAsia · ถึง 08:15 น. (1 ชม. 15 น.) · ผู้โดยสาร 2 คน"
                },
                {
                    "id": "p6",
                    "name": "ถึงสนามบินสุราษฎร์ธานี (URT)",
                    "lat": 9.1342, "lng": 99.1354,
                    "time": "08:15",
                    "note": "ลงเครื่องแล้ว"
                },
                {
                    "id": "p7",
                    "name": "นั่งรถไปท่าเรือดอนสัก",
                    "lat": 9.3167829, "lng": 99.7246064,
                    "time": "10:30",
                    "note": "ใช้เวลาประมาณ 1 ชม. 30 นาที"
                },
                {
                    "id": "p8",
                    "name": "นั่งเรือไปท่าเรือหน้าทอน เกาะสมุย",
                    "lat": 9.536353, "lng": 99.9331332,
                    "time": "12:00",
                    "note": "เรือเฟอร์รี่ ใช้เวลาประมาณ 1 ชม. 30 นาที"
                },
                {
                    "id": "p10",
                    "name": "กินข้าวที่ร้านกะปิ สะตอ",
                    "lat": 9.5358252, "lng": 100.0364703,
                    "time": "13:00",
                    "note": "มื้อกลางวัน อาหารใต้"
                },
                {
                    "id": "p11",
                    "name": "เดินเล่นที่เซ็นทรัล สมุย",
                    "lat": 9.5326483, "lng": 100.0618091,
                    "time": "14:30",
                    "note": "เดินเล่น รอเวลาเช็คอิน"
                },
                {
                    "id": "p3",
                    "name": "เช็คอิน COSI Samui Chaweng Beach",
                    "lat": 9.5311554, "lng": 100.0578517,
                    "time": "15:00",
                    "note": "เกาะสมุย · 1 ห้อง"
                },
                {
                    "id": "p12",
                    "name": "กินข้าวและดูไฟที่ Coco Tam",
                    "lat": 9.5598146, "lng": 100.0263889,
                    "time": "17:30",
                    "note": "บาร์ริมหาดบ่อผุด มื้อเย็น + ดูไฟโชว์"
                }
            ]
        },
        {"id": "d2", "label": "วันที่ 2", "date": "2026-07-26", "places": []},
        {"id": "d3", "label": "วันที่ 3", "date": "2026-07-27", "places": []},
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
                    "note": ""
                },
                {
                    "id": "p5",
                    "name": "เที่ยวบิน DD 575 · สุราษฎร์ธานี (URT) → ดอนเมือง (DMK)",
                    "lat": 9.1342, "lng": 99.1354,
                    "time": "15:20",
                    "note": "Nok Air · ถึง 16:35 น. (1 ชม. 15 น.) · ผู้โดยสาร 2 คน"
                }
            ]
        }
    ]
}


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
  .icon-btn{
    background:var(--surface-2);color:var(--text);padding:8px 14px;border-radius:999px;font-size:13px;font-weight:600;
    transition:background .15s ease, color .15s ease, transform .1s ease;
  }
  .icon-btn:hover{background:var(--accent-soft);color:var(--accent);}
  .icon-btn:active{transform:scale(0.96);}

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
  .map-pin-dot{width:16px;height:16px;border-radius:50%;border:3px solid var(--surface);box-shadow:var(--shadow-sm);flex-shrink:0;}
  .map-pin-connector{width:12px;height:2px;flex-shrink:0;}
  .map-pin-card{
    background:var(--surface);border:1px solid var(--border);border-left-width:4px;border-radius:10px;
    padding:5px 10px;box-shadow:var(--shadow-md);max-width:170px;font-family:'Inter',system-ui,sans-serif;
  }
  .map-pin-card .pnum{font-weight:800;font-size:11px;margin-right:4px;}
  .map-pin-card .pname{font-weight:600;font-size:12px;color:var(--text);line-height:1.3;display:inline;}
  .map-pin-card .ptime{font-size:10.5px;font-weight:700;margin-top:2px;}

  .toast{
    position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--text);color:var(--bg);
    padding:11px 20px;border-radius:999px;font-size:13px;font-weight:500;z-index:2000;opacity:0;pointer-events:none;
    transition:opacity .25s ease; box-shadow:var(--shadow-md);
  }
  .toast.show{opacity:1;}
</style>
</head>
<body>
<div id="app"></div>
<div id="toast" class="toast"></div>

<script>
  let TRIP = {{ trip | tojson }};

  const PALETTE = ['#4F46E5','#F97316','#10B981','#EC4899','#0EA5E9','#EAB308'];
  const app = document.getElementById('app');
  const toastEl = document.getElementById('toast');

  let state = { trip: TRIP, selectedDayId: TRIP.days[0] ? TRIP.days[0].id : null,
                map: null, markersLayer: null, routeLayer: null, markersById: {} };

  function showToast(msg){ toastEl.textContent = msg; toastEl.classList.add('show'); setTimeout(()=> toastEl.classList.remove('show'), 1800); }
  function escapeHtml(s){ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function currentDay(){ return state.trip.days.find(d=>d.id===state.selectedDayId) || state.trip.days[0]; }
  function dayColor(idx){ return PALETTE[((idx%PALETTE.length)+PALETTE.length)%PALETTE.length]; }

  function renderTrip(){
    const trip = state.trip;
    app.innerHTML = `
      <div class="trip-header">
        <div class="trip-title-static">${escapeHtml(trip.name)}</div>
        <div class="header-spacer"></div>
        <button class="icon-btn" id="btn-refresh">รีเฟรช</button>
        <button class="icon-btn" id="btn-share">แชร์ลิงก์</button>
      </div>
      <div class="trip-body">
        <div class="side-panel">
          <div class="day-tabs" id="day-tabs"></div>
          <div class="day-label-row" id="day-field-row"></div>
          <ul class="place-list" id="place-list"></ul>
        </div>
        <div id="map"></div>
      </div>`;

    document.getElementById('btn-refresh').onclick = ()=> location.reload();
    document.getElementById('btn-share').onclick = ()=>{
      navigator.clipboard.writeText(window.location.href).then(()=> showToast('คัดลอกลิงก์แล้ว ส่งให้คนอื่นดูได้เลย'));
    };

    renderDayTabs(); renderDayFields(); renderPlaceList(); initMapIfNeeded(); updateMapMarkers();
  }

  function renderDayTabs(){
    const wrap = document.getElementById('day-tabs'); const trip = state.trip;
    wrap.innerHTML = trip.days.map(d=>`
      <button class="day-tab ${d.id===state.selectedDayId?'active':''}" data-day="${d.id}">${escapeHtml(d.label)}</button>`).join('');

    wrap.querySelectorAll('.day-tab').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        state.selectedDayId = btn.dataset.day;
        renderDayFields(); renderPlaceList(); updateMapMarkers();
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
    list.innerHTML = day.places.map((p,i)=>`
      <li class="place-item" data-place="${p.id}" style="border-left-color:${dayColor(state.trip.days.indexOf(day))}">
        <div class="place-top">
          <div class="place-num" style="background:${dayColor(state.trip.days.indexOf(day))}">${i+1}</div>
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
  }

  function initMapIfNeeded(){
    if(state.map){ state.map.remove(); state.map = null; }
    state.map = L.map('map', {zoomControl:true}).setView([13.7563,100.5018], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19, attribution:'&copy; OpenStreetMap contributors'}).addTo(state.map);
    state.markersLayer = L.layerGroup().addTo(state.map);
    state.routeLayer = L.layerGroup().addTo(state.map);
    const allPlaces = state.trip.days.flatMap(d=>d.places);
    if(allPlaces.length){
      const bounds = L.latLngBounds(allPlaces.map(p=>[p.lat,p.lng]));
      state.map.fitBounds(bounds, {padding:[40,40]});
    }
  }

  function labelIcon(color, num, name, time, side){
    const shortName = name.length > 30 ? name.slice(0,29)+'…' : name;
    const cardHtml = `<div class="map-pin-card" style="border-color:${color}">
        <span class="pnum" style="color:${color}">${num}</span><span class="pname">${escapeHtml(shortName)}</span>
        ${time?`<div class="ptime" style="color:${color}">${escapeHtml(time)} น.</div>`:''}
      </div>`;
    const dotHtml = `<div class="map-pin-dot" style="background:${color}"></div>`;
    const connectorHtml = `<div class="map-pin-connector" style="background:${color}"></div>`;
    let html, anchorX;
    if(side==='left'){
      html = `<div style="display:flex;align-items:center;justify-content:flex-end;height:44px;">${cardHtml}${connectorHtml}${dotHtml}</div>`;
      anchorX = 191;
    } else {
      html = `<div style="display:flex;align-items:center;height:44px;">${dotHtml}${connectorHtml}${cardHtml}</div>`;
      anchorX = 9;
    }
    return L.divIcon({className:'', html, iconSize:[200,44], iconAnchor:[anchorX,22]});
  }

  let routeRequestId = 0;
  function isDirectLeg(a,b){
    // เที่ยวบิน = leg starting at a flight pin is the flight itself (not a road)
    // นั่งเรือ = leg arriving at a ferry-ride pin is the sea crossing (routing engines
    // often snap it to the wrong ferry pier, so draw it direct instead)
    return /เที่ยวบิน/.test(a.name) || /นั่งเรือ/.test(b.name);
  }

  async function fetchRoadRoute(a, b){
    try{
      const url = `https://router.project-osrm.org/route/v1/driving/${a[1]},${a[0]};${b[1]},${b[0]}?overview=full&geometries=geojson`;
      const r = await fetch(url);
      const data = await r.json();
      if(data.code === 'Ok' && data.routes && data.routes[0]){
        return data.routes[0].geometry.coordinates.map(c=>[c[1],c[0]]);
      }
    }catch(e){ /* fall back to straight line below */ }
    return [a, b];
  }

  async function updateMapMarkers(){
    if(!state.map) return;
    const myRequestId = ++routeRequestId;
    state.markersLayer.clearLayers(); state.routeLayer.clearLayers();
    state.markersById = {};
    const day = currentDay(); const dayIdx = day ? state.trip.days.indexOf(day) : 0; const color = dayColor(dayIdx);
    if(!day) return;

    day.places.forEach((p,i)=>{
      const side = i % 2 === 0 ? 'right' : 'left';
      const marker = L.marker([p.lat,p.lng], {icon:labelIcon(color,i+1,p.name,p.time,side)})
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
