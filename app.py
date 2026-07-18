"""
วางแพลนเที่ยว — Flask trip planner
-----------------------------------
เว็บแอปวางแผนทริปหน้าเดียว: แผนที่ + ปักหมุด + ไทม์ไลน์รายวัน
- คนเดียว (คุณ) แก้ไขได้ผ่านรหัสผ่าน ส่วนคนอื่นที่เปิดลิงก์เว็บนี้จะเห็นแบบดูอย่างเดียว
- ข้อมูลเก็บลงไฟล์ trip_data.json บนเซิร์ฟเวอร์ (สร้างอัตโนมัติถ้ายังไม่มี)

รันเทสต์ในเครื่อง:
    pip install -r requirements.txt
    python app.py
    เปิด http://localhost:5000

Deploy ดูวิธีได้ใน README.md
"""

import json
import os
import threading
from flask import Flask, request, jsonify, session, render_template_string

app = Flask(__name__)
# สำคัญ: ตอน deploy จริง ตั้งค่า environment variable SECRET_KEY เป็นค่าสุ่มของตัวเอง
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-please-change-me")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "trip_data.json")
_lock = threading.Lock()

# ---------------------------------------------------------------------------
# ข้อมูลเริ่มต้นของทริป — แก้รหัสผ่านตรง "passcode" ก่อน deploy จริงด้วยนะ
# ---------------------------------------------------------------------------
DEFAULT_TRIP = {
    "name": "ทริปเกาะสมุย <3",
    "passcode": "bestdream2312",
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
                    "lat": 9.2028, "lng": 99.6893,
                    "time": "09:00",
                    "note": "ใช้เวลาประมาณ 1 ชม. 30 นาที"
                },
                {
                    "id": "p8",
                    "name": "นั่งเรือไปท่าเรือหน้าทอน เกาะสมุย",
                    "lat": 9.5350, "lng": 99.9556,
                    "time": "10:30",
                    "note": "เรือเฟอร์รี่ ใช้เวลาประมาณ 1 ชม. 30 นาที"
                },
                {
                    "id": "p3",
                    "name": "เช็คอิน COSI Samui Chaweng Beach",
                    "lat": 9.5518, "lng": 100.0453,
                    "time": "15:00",
                    "note": "เกาะสมุย · 1 ห้อง"
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
                    "lat": 9.5518, "lng": 100.0453,
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


def load_trip():
    with _lock:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_TRIP, f, ensure_ascii=False, indent=2)
            return json.loads(json.dumps(DEFAULT_TRIP))
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)


def save_trip(trip):
    with _lock:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(trip, f, ensure_ascii=False, indent=2)


def valid_trip_payload(data):
    if not isinstance(data, dict):
        return False
    if "name" not in data or "days" not in data or "passcode" not in data:
        return False
    if not isinstance(data["days"], list):
        return False
    for d in data["days"]:
        if not isinstance(d, dict) or "id" not in d or "places" not in d:
            return False
        if not isinstance(d["places"], list):
            return False
    return True


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    trip = load_trip()
    is_editor = bool(session.get("editor", False))
    return render_template_string(PAGE_TEMPLATE, trip=trip, is_editor=is_editor)


@app.route("/api/trip", methods=["GET"])
def api_get_trip():
    trip = load_trip()
    safe_trip = dict(trip)
    safe_trip.pop("passcode", None)  # ไม่ส่งรหัสผ่านออกไปให้ฝั่งไคลเอนต์
    return jsonify({"trip": safe_trip, "is_editor": bool(session.get("editor", False))})


@app.route("/api/trip", methods=["POST"])
def api_save_trip():
    if not session.get("editor"):
        return jsonify({"error": "ไม่มีสิทธิ์แก้ไข"}), 403
    incoming = request.get_json(force=True, silent=True)
    if not incoming or not isinstance(incoming, dict) or "days" not in incoming:
        return jsonify({"error": "ข้อมูลไม่ถูกต้อง"}), 400
    current = load_trip()
    current["name"] = str(incoming.get("name", current["name"]))[:120]
    current["days"] = incoming["days"]
    if not valid_trip_payload(current):
        return jsonify({"error": "ข้อมูลไม่ถูกต้อง"}), 400
    save_trip(current)
    return jsonify({"ok": True})


@app.route("/api/unlock", methods=["POST"])
def api_unlock():
    data = request.get_json(force=True, silent=True) or {}
    passcode = str(data.get("passcode", ""))
    trip = load_trip()
    if passcode and passcode == trip.get("passcode"):
        session["editor"] = True
        session.permanent = True
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "รหัสผ่านไม่ถูกต้อง"}), 401


@app.route("/api/lock", methods=["POST"])
def api_lock():
    session["editor"] = False
    return jsonify({"ok": True})


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
<style>
  :root{
    --paper:#F2EDE1; --paper-2:#E9E1CF; --teal:#1B4B43; --teal-deep:#123530;
    --teal-light:#CBE0DA; --mustard:#E3A72C; --coral:#D6572A; --ink:#232323; --white:#FFFFFF;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    font-family:Georgia,'Noto Serif Thai',serif; color:var(--ink); background:var(--paper);
    background-image:radial-gradient(circle at 1px 1px, rgba(27,75,67,0.08) 1px, transparent 0);
    background-size:22px 22px;
  }
  .display{font-family:'Arial Black','Trebuchet MS',sans-serif;text-transform:uppercase;letter-spacing:0.02em;font-weight:900;}
  button{font-family:inherit;cursor:pointer;border:none;}
  input{font-family:inherit;}
  .field{margin-bottom:12px;}
  .field label{display:block;font-size:12px;text-transform:uppercase;letter-spacing:0.06em;color:var(--teal-deep);margin-bottom:4px;font-weight:bold;}
  .field input{width:100%;padding:9px 10px;border:1.5px solid var(--teal-light);border-radius:3px;font-size:14px;background:var(--paper);}
  .field input:focus{outline:2px solid var(--coral);outline-offset:1px;}
  .btn{display:inline-block;padding:10px 18px;border-radius:3px;font-size:14px;font-weight:bold;letter-spacing:0.03em;}
  .btn-primary{background:var(--coral);color:var(--white);}
  .btn-primary:hover{background:#bf4a20;}
  .btn-ghost{background:transparent;color:var(--teal);border:1.5px solid var(--teal);}
  .btn-ghost:hover{background:var(--teal-light);}
  .btn-block{width:100%;text-align:center;}
  .error-msg{color:var(--coral);font-size:13px;margin-top:6px;min-height:16px;}

  .trip-header{
    background:var(--teal);color:var(--white);padding:14px 20px;display:flex;align-items:center;gap:14px;
    flex-wrap:wrap;position:sticky;top:0;z-index:500;border-bottom:3px solid var(--mustard);
  }
  .trip-title-input,.trip-title-static{
    background:transparent;border:none;color:var(--white);font-family:'Arial Black','Trebuchet MS',sans-serif;
    text-transform:uppercase;font-size:20px;font-weight:900;letter-spacing:0.02em;padding:2px 4px;max-width:320px;
  }
  .trip-title-input:focus{outline:1.5px dashed var(--mustard);}
  .mode-badge{padding:5px 10px;border-radius:3px;font-size:12px;font-weight:bold;letter-spacing:0.05em;}
  .mode-badge.edit{background:var(--mustard);color:var(--teal-deep);}
  .mode-badge.view{background:rgba(255,255,255,0.15);color:var(--white);}
  .header-spacer{flex:1;}
  .icon-btn{background:rgba(255,255,255,0.12);color:var(--white);padding:7px 12px;border-radius:3px;font-size:13px;}
  .icon-btn:hover{background:rgba(255,255,255,0.24);}

  .trip-body{display:grid;grid-template-columns:340px 1fr;gap:0;min-height:calc(100vh - 62px);}
  @media (max-width:860px){ .trip-body{grid-template-columns:1fr;} #map{height:340px !important;} }
  .side-panel{background:var(--paper-2);border-right:2px solid var(--teal-light);padding:16px;overflow-y:auto;}
  .day-tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;}
  .day-tab{background:var(--white);border:1.5px solid var(--teal);color:var(--teal);padding:6px 12px;border-radius:20px;font-size:13px;font-weight:bold;position:relative;}
  .day-tab.active{background:var(--teal);color:var(--white);}
  .day-tab .del-x{margin-left:6px;opacity:0.6;}
  .day-tab-add{background:var(--mustard);border:1.5px solid var(--mustard);color:var(--teal-deep);width:30px;height:30px;border-radius:50%;font-size:16px;font-weight:bold;line-height:1;}
  .day-label-row{display:flex;align-items:center;gap:8px;margin-bottom:10px;}
  .day-label-input,.day-label-static{flex:1;border:none;background:transparent;font-size:16px;font-weight:bold;color:var(--teal-deep);border-bottom:1.5px dashed var(--teal-light);padding:2px 0;}
  .day-label-static{border-bottom:none;}
  .day-date-input{border:1.5px solid var(--teal-light);border-radius:3px;padding:4px 6px;font-size:12px;background:var(--white);}
  .day-date-static{font-size:12px;opacity:0.65;}
  .hint{font-size:12.5px;color:var(--teal-deep);opacity:0.7;background:var(--teal-light);padding:8px 10px;border-radius:4px;margin-bottom:12px;}
  .place-list{list-style:none;margin:0;padding:0;}
  .place-item{background:var(--white);border:1.5px solid var(--teal-light);border-left:5px solid var(--coral);border-radius:3px;padding:10px 12px;margin-bottom:8px;}
  .place-top{display:flex;align-items:flex-start;gap:8px;}
  .place-num{background:var(--coral);color:var(--white);width:22px;height:22px;border-radius:50%;font-size:12px;font-weight:bold;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;}
  .place-main{flex:1;min-width:0;}
  .place-name{font-weight:bold;font-size:14px;color:var(--teal-deep);}
  .place-time{font-size:12px;color:var(--coral);font-weight:bold;}
  .place-note{font-size:12.5px;opacity:0.75;margin-top:2px;}
  .place-actions{display:flex;gap:4px;flex-shrink:0;}
  .place-actions button{background:var(--paper-2);color:var(--teal-deep);width:24px;height:24px;border-radius:3px;font-size:12px;}
  .place-actions button:hover{background:var(--teal-light);}
  .empty-state{text-align:center;padding:30px 10px;color:var(--teal-deep);opacity:0.55;font-size:13.5px;}
  .unlock-box{margin-top:18px;padding:12px;border:1.5px dashed var(--teal-light);border-radius:4px;}
  .unlock-box p{font-size:12px;opacity:0.7;margin:0 0 8px;}

  #map{height:calc(100vh - 62px);width:100%;}
  .map-pin-dot{width:18px;height:18px;border-radius:50%;border:2.5px solid var(--white);box-shadow:1px 1px 3px rgba(0,0,0,0.35);flex-shrink:0;}
  .map-pin-connector{width:14px;height:2.5px;flex-shrink:0;}
  .map-pin-card{background:var(--white);border:1.5px solid;border-left-width:5px;border-radius:4px;padding:4px 9px;box-shadow:2px 2px 5px rgba(0,0,0,0.22);max-width:158px;font-family:Georgia,'Noto Serif Thai',serif;}
  .map-pin-card .pnum{font-weight:900;font-size:11px;margin-right:3px;}
  .map-pin-card .pname{font-weight:bold;font-size:12px;color:var(--ink);line-height:1.25;display:inline;}
  .map-pin-card .ptime{font-size:10.5px;font-weight:bold;margin-top:2px;}

  .modal-backdrop{position:fixed;inset:0;background:rgba(18,53,48,0.55);display:flex;align-items:center;justify-content:center;z-index:1000;padding:16px;}
  .modal{background:var(--white);border-radius:6px;border:2px solid var(--teal);padding:22px;width:100%;max-width:380px;box-shadow:8px 8px 0 var(--mustard);}
  .modal h3{margin:0 0 14px;color:var(--teal);font-size:18px;}
  .modal-actions{display:flex;gap:8px;margin-top:16px;}
  .modal-actions .btn{flex:1;text-align:center;}
  .toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:var(--teal-deep);color:var(--white);padding:10px 18px;border-radius:20px;font-size:13px;z-index:2000;opacity:0;pointer-events:none;transition:opacity 0.25s ease;}
  .toast.show{opacity:1;}
</style>
</head>
<body>
<div id="app"></div>
<div id="toast" class="toast"></div>

<script>
  let TRIP = {{ trip | tojson }};
  let IS_EDITOR = {{ 'true' if is_editor else 'false' }};
  delete TRIP.passcode;

  const PALETTE = ['#D6572A','#1B4B43','#E3A72C','#5B7A8C','#8C5B7A','#4E7B3E'];
  const app = document.getElementById('app');
  const toastEl = document.getElementById('toast');

  let state = { trip: TRIP, isEditor: IS_EDITOR, selectedDayId: TRIP.days[0] ? TRIP.days[0].id : null,
                showAllDays: false, map: null, markersLayer: null, routeLayer: null };

  function showToast(msg){ toastEl.textContent = msg; toastEl.classList.add('show'); setTimeout(()=> toastEl.classList.remove('show'), 1800); }
  function uid(){ return Math.random().toString(36).slice(2,10); }
  function escapeAttr(s){ return (s||'').replace(/"/g,'&quot;'); }
  function escapeHtml(s){ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  async function apiGetTrip(){
    const r = await fetch('/api/trip'); return r.json();
  }
  let saveTimer = null;
  function scheduleSave(){
    if(!state.isEditor) return;
    if(saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(async ()=>{
      try{
        const r = await fetch('/api/trip', {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({name: state.trip.name, days: state.trip.days})
        });
        if(!r.ok){ showToast('บันทึกไม่สำเร็จ ลองรีเฟรชแล้วเข้าโหมดแก้ไขใหม่'); }
      }catch(e){ showToast('บันทึกไม่สำเร็จ (ออฟไลน์?)'); }
    }, 350);
  }

  function currentDay(){ return state.trip.days.find(d=>d.id===state.selectedDayId) || state.trip.days[0]; }
  function dayColor(idx){ return PALETTE[((idx%PALETTE.length)+PALETTE.length)%PALETTE.length]; }

  function renderTrip(){
    const trip = state.trip; const editing = state.isEditor;
    app.innerHTML = `
      <div class="trip-header">
        ${editing ? `<input class="trip-title-input display" id="trip-name-input" value="${escapeAttr(trip.name)}" />`
                  : `<div class="trip-title-static display">${escapeHtml(trip.name)}</div>`}
        ${editing ? `<div class="mode-badge edit">โหมดแก้ไข</div>` : ''}
        <div class="header-spacer"></div>
        <button class="icon-btn" id="btn-refresh">รีเฟรช</button>
        <button class="icon-btn" id="btn-share">แชร์ลิงก์</button>
        ${editing ? `<button class="icon-btn" id="btn-exit-edit">ออกจากโหมดแก้ไข</button>` : ''}
      </div>
      <div class="trip-body">
        <div class="side-panel">
          <div class="day-tabs" id="day-tabs"></div>
          <div class="day-label-row" id="day-field-row"></div>
          ${editing ? `<div class="hint">คลิกบนแผนที่เพื่อปักหมุดสถานที่ในวันนี้</div>` : ''}
          <ul class="place-list" id="place-list"></ul>
          ${editing ? `
            <label style="display:flex;align-items:center;gap:8px;font-size:12.5px;margin-top:14px;color:var(--teal-deep);">
              <input type="checkbox" id="toggle-all-days" ${state.showAllDays?'checked':''}/>
              แสดงหมุดทุกวันบนแผนที่ (จาง ๆ)
            </label>` : ''}
          ${!editing ? `
            <div class="unlock-box">
              <p>เป็นเจ้าของทริปนี้ใช่ไหม? ปลดล็อกโหมดแก้ไขด้วยรหัสผ่าน</p>
              <button class="btn btn-ghost btn-block" id="btn-unlock">ปลดล็อกโหมดแก้ไข</button>
            </div>` : ''}
        </div>
        <div id="map"></div>
      </div>`;

    document.getElementById('btn-refresh').onclick = async ()=>{
      const res = await apiGetTrip();
      state.trip = res.trip; state.isEditor = res.is_editor;
      if(!state.trip.days.find(d=>d.id===state.selectedDayId)){
        state.selectedDayId = state.trip.days[0] ? state.trip.days[0].id : null;
      }
      renderTrip(); showToast('อัปเดตข้อมูลล่าสุดแล้ว');
    };
    document.getElementById('btn-share').onclick = ()=>{
      navigator.clipboard.writeText(window.location.href).then(()=> showToast('คัดลอกลิงก์แล้ว ส่งให้คนอื่นดูได้เลย'));
    };
    if(editing){
      document.getElementById('trip-name-input').onchange = (e)=>{ state.trip.name = e.target.value.trim() || state.trip.name; scheduleSave(); };
      document.getElementById('btn-exit-edit').onclick = async ()=>{
        await fetch('/api/lock', {method:'POST'}); state.isEditor = false; renderTrip();
      };
      const toggleAll = document.getElementById('toggle-all-days');
      if(toggleAll){ toggleAll.onchange = (e)=>{ state.showAllDays = e.target.checked; updateMapMarkers(); }; }
    } else {
      document.getElementById('btn-unlock').onclick = openUnlockModal;
    }

    renderDayTabs(); renderDayFields(); renderPlaceList(); initMapIfNeeded(); updateMapMarkers();
  }

  function renderDayTabs(){
    const wrap = document.getElementById('day-tabs'); const trip = state.trip; const editing = state.isEditor;
    wrap.innerHTML = trip.days.map(d=>`
      <button class="day-tab ${d.id===state.selectedDayId?'active':''}" data-day="${d.id}">
        ${escapeHtml(d.label)}
        ${(editing && trip.days.length>1) ? `<span class="del-x" data-del="${d.id}">✕</span>` : ''}
      </button>`).join('') + (editing ? `<button class="day-tab-add" id="btn-add-day">+</button>` : '');

    wrap.querySelectorAll('.day-tab').forEach(btn=>{
      btn.addEventListener('click', (e)=>{
        if(e.target.dataset.del) return;
        state.selectedDayId = btn.dataset.day;
        renderDayFields(); renderPlaceList(); updateMapMarkers();
        wrap.querySelectorAll('.day-tab').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
      });
    });
    wrap.querySelectorAll('[data-del]').forEach(x=>{
      x.addEventListener('click', (e)=>{
        e.stopPropagation();
        const id = x.dataset.del;
        if(!confirm('ลบวันนี้ทั้งหมด รวมสถานที่ที่ปักไว้?')) return;
        state.trip.days = state.trip.days.filter(d=>d.id!==id);
        if(state.selectedDayId===id){ state.selectedDayId = state.trip.days[0] ? state.trip.days[0].id : null; }
        scheduleSave(); renderDayTabs(); renderDayFields(); renderPlaceList(); updateMapMarkers();
      });
    });
    if(editing){
      document.getElementById('btn-add-day').onclick = ()=>{
        const n = state.trip.days.length + 1;
        const nd = {id:'d'+uid(), label:'วันที่ '+n, date:'', places:[]};
        state.trip.days.push(nd); state.selectedDayId = nd.id;
        scheduleSave(); renderDayTabs(); renderDayFields(); renderPlaceList(); updateMapMarkers();
      };
    }
  }

  function renderDayFields(){
    const day = currentDay(); const row = document.getElementById('day-field-row'); const editing = state.isEditor;
    if(!day){ row.innerHTML = ''; return; }
    if(editing){
      row.innerHTML = `
        <input class="day-label-input" id="day-label-input" value="${escapeAttr(day.label)}" />
        <input class="day-date-input" id="day-date-input" type="date" value="${escapeAttr(day.date||'')}" />`;
      document.getElementById('day-label-input').onchange = (e)=>{ day.label = e.target.value.trim() || day.label; scheduleSave(); renderDayTabs(); };
      document.getElementById('day-date-input').onchange = (e)=>{ day.date = e.target.value; scheduleSave(); };
    } else {
      row.innerHTML = `<div class="day-label-static">${escapeHtml(day.label)}</div>${day.date?`<div class="day-date-static">${escapeHtml(day.date)}</div>`:''}`;
    }
  }

  function renderPlaceList(){
    const list = document.getElementById('place-list'); const day = currentDay(); const editing = state.isEditor;
    if(!day || day.places.length===0){
      list.innerHTML = `<div class="empty-state">${editing?'ยังไม่มีสถานที่ในวันนี้<br/>คลิกบนแผนที่เพื่อเริ่มปักหมุด':'ยังไม่มีสถานที่ในวันนี้'}</div>`;
      return;
    }
    list.innerHTML = day.places.map((p,i)=>`
      <li class="place-item" style="border-left-color:${dayColor(state.trip.days.indexOf(day))}">
        <div class="place-top">
          <div class="place-num" style="background:${dayColor(state.trip.days.indexOf(day))}">${i+1}</div>
          <div class="place-main">
            <div class="place-name">${escapeHtml(p.name)}</div>
            ${p.time?`<div class="place-time">${escapeHtml(p.time)} น.</div>`:''}
            ${p.note?`<div class="place-note">${escapeHtml(p.note)}</div>`:''}
          </div>
          ${editing?`<div class="place-actions">
            <button data-up="${p.id}" title="เลื่อนขึ้น">↑</button>
            <button data-down="${p.id}" title="เลื่อนลง">↓</button>
            <button data-del="${p.id}" title="ลบ">✕</button>
          </div>`:''}
        </div>
      </li>`).join('');
    if(editing){
      list.querySelectorAll('[data-up]').forEach(b=> b.onclick = ()=> movePlace(b.dataset.up,-1));
      list.querySelectorAll('[data-down]').forEach(b=> b.onclick = ()=> movePlace(b.dataset.down,1));
      list.querySelectorAll('[data-del]').forEach(b=> b.onclick = ()=> deletePlace(b.dataset.del));
    }
  }

  function movePlace(placeId, dir){
    const day = currentDay(); const idx = day.places.findIndex(p=>p.id===placeId); const newIdx = idx+dir;
    if(newIdx<0 || newIdx>=day.places.length) return;
    const tmp = day.places[idx]; day.places[idx]=day.places[newIdx]; day.places[newIdx]=tmp;
    scheduleSave(); renderPlaceList(); updateMapMarkers();
  }
  function deletePlace(placeId){
    const day = currentDay(); day.places = day.places.filter(p=>p.id!==placeId);
    scheduleSave(); renderPlaceList(); updateMapMarkers();
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
    if(state.isEditor){
      state.map.on('click', (e)=> openAddPlaceModal(e.latlng.lat, e.latlng.lng));
    }
  }

  function flagIcon(color, num){
    return L.divIcon({
      className:'', iconSize:[22,22], iconAnchor:[11,22],
      html:`<div style="display:flex;flex-direction:column;align-items:center;transform:translateY(-6px);">
              <div style="background:${color};color:#fff;border:2px solid #fff;width:20px;height:20px;border-radius:50% 50% 50% 0;transform:rotate(45deg);display:flex;align-items:center;justify-content:center;box-shadow:1px 1px 3px rgba(0,0,0,.35);">
                <span style="transform:rotate(-45deg);font-size:10px;font-weight:bold;">${num}</span>
              </div></div>`
    });
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

  function updateMapMarkers(){
    if(!state.map) return;
    state.markersLayer.clearLayers(); state.routeLayer.clearLayers();
    const day = currentDay(); const dayIdx = day ? state.trip.days.indexOf(day) : 0; const color = dayColor(dayIdx);

    if(state.isEditor && state.showAllDays){
      state.trip.days.forEach((d,di)=>{
        if(d.id === (day&&day.id)) return;
        const c = dayColor(di);
        d.places.forEach((p,i)=>{
          L.marker([p.lat,p.lng], {icon:flagIcon(c,i+1), opacity:0.4})
            .bindPopup(`<b>${escapeHtml(p.name)}</b><br/>${escapeHtml(d.label)}`).addTo(state.markersLayer);
        });
      });
    }
    if(day){
      const latlngs = [];
      day.places.forEach((p,i)=>{
        latlngs.push([p.lat,p.lng]);
        const side = i % 2 === 0 ? 'right' : 'left';
        L.marker([p.lat,p.lng], {icon:labelIcon(color,i+1,p.name,p.time,side)})
          .bindPopup(`<b>${escapeHtml(p.name)}</b>${p.time?`<br/>${escapeHtml(p.time)} น.`:''}${p.note?`<br/>${escapeHtml(p.note)}`:''}`)
          .addTo(state.markersLayer);
      });
      if(latlngs.length>1){ L.polyline(latlngs, {color:color, weight:3, dashArray:'6 8', opacity:0.85}).addTo(state.routeLayer); }
    }
  }

  function openAddPlaceModal(lat,lng){
    const day = currentDay(); if(!day){ showToast('เพิ่มวันก่อนนะ'); return; }
    const backdrop = document.createElement('div'); backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `
      <div class="modal">
        <h3>ปักหมุดสถานที่ — ${escapeHtml(day.label)}</h3>
        <div class="field"><label>ชื่อสถานที่</label><input id="modal-place-name" type="text" placeholder="เช่น หาดเฉวง" /></div>
        <div class="field"><label>เวลา (ไม่บังคับ)</label><input id="modal-place-time" type="time" /></div>
        <div class="field"><label>โน้ต (ไม่บังคับ)</label><input id="modal-place-note" type="text" placeholder="เช่น ไปตอนเช้าคนน้อย" /></div>
        <div class="modal-actions">
          <button class="btn btn-ghost" id="modal-cancel">ยกเลิก</button>
          <button class="btn btn-primary" id="modal-save">ปักหมุด</button>
        </div>
      </div>`;
    document.body.appendChild(backdrop);
    document.getElementById('modal-place-name').focus();
    const close = ()=> backdrop.remove();
    document.getElementById('modal-cancel').onclick = close;
    backdrop.addEventListener('click', (e)=>{ if(e.target===backdrop) close(); });
    document.getElementById('modal-save').onclick = ()=>{
      const name = document.getElementById('modal-place-name').value.trim();
      const time = document.getElementById('modal-place-time').value;
      const note = document.getElementById('modal-place-note').value.trim();
      if(!name){ document.getElementById('modal-place-name').focus(); return; }
      day.places.push({id:'p'+uid(), name, lat, lng, time, note});
      scheduleSave(); renderPlaceList(); updateMapMarkers(); close();
    };
  }

  function openUnlockModal(){
    const backdrop = document.createElement('div'); backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `
      <div class="modal">
        <h3>ปลดล็อกโหมดแก้ไข</h3>
        <div class="field"><label>รหัสผ่าน</label><input id="modal-passcode" type="password" placeholder="รหัสผ่านของทริปนี้" /></div>
        <div class="error-msg" id="unlock-error"></div>
        <div class="modal-actions">
          <button class="btn btn-ghost" id="unlock-cancel">ยกเลิก</button>
          <button class="btn btn-primary" id="unlock-confirm">ปลดล็อก</button>
        </div>
      </div>`;
    document.body.appendChild(backdrop);
    document.getElementById('modal-passcode').focus();
    const close = ()=> backdrop.remove();
    document.getElementById('unlock-cancel').onclick = close;
    backdrop.addEventListener('click', (e)=>{ if(e.target===backdrop) close(); });
    document.getElementById('unlock-confirm').onclick = async ()=>{
      const val = document.getElementById('modal-passcode').value;
      try{
        const r = await fetch('/api/unlock', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({passcode: val})});
        const data = await r.json();
        if(!r.ok || !data.ok){ document.getElementById('unlock-error').textContent = data.error || 'รหัสผ่านไม่ถูกต้อง'; return; }
        state.isEditor = true; close(); renderTrip(); showToast('ปลดล็อกโหมดแก้ไขแล้ว');
      }catch(e){ document.getElementById('unlock-error').textContent = 'เชื่อมต่อไม่สำเร็จ'; }
    };
  }

  renderTrip();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
