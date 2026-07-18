# วางแพลนเที่ยว — Flask Trip Planner

เว็บแอปวางแผนทริปหน้าเดียว: แผนที่ + ปักหมุด + ไทม์ไลน์รายวัน
เป็นเว็บแบบ **ดูอย่างเดียว** — ไม่มีโหมดแก้ไขบนเว็บ ใครเปิดลิงก์ก็ดูแผนได้เหมือนกันหมด

ข้อมูลทริปตอนนี้ตั้งต้นไว้ให้แล้ว: เริ่มจากคอนโด The President สาทร-ราชพฤกษ์ เฟส 3 → สนามบินดอนเมือง (เที่ยวบิน FD 3235) → ลงสนามบินสุราษฎร์ธานี → รถไปท่าเรือดอนสัก → เรือไปท่าเรือหน้าทอน → เช็คอิน COSI Samui Chaweng Beach (วันที่ 1) และเช็คเอาต์ + เที่ยวบิน DD 575 กลับ (วันที่ 4) ส่วนวันที่ 2-3 เว้นว่างไว้

## จะแก้แผนทริปยังไง

ไม่มีโหมดแก้ไขบนเว็บแล้ว — แก้ได้ทางเดียวคือแก้ `DEFAULT_TRIP` ในไฟล์ `app.py` แล้ว commit + push ขึ้น GitHub เพื่อให้ Render deploy ใหม่ (บอกในแชทกับ Claude ได้เลยว่าจะแก้อะไร)

## รันทดสอบในเครื่องตัวเอง

```bash
pip install -r requirements.txt
python app.py
```

เปิด http://localhost:5000

## Deploy ให้คนอื่นเข้าดูได้ (แนะนำ: Render.com — ฟรี)

1. สร้าง repo บน GitHub แล้วอัปโหลดไฟล์ทั้งหมดในโฟลเดอร์นี้ (`app.py`, `requirements.txt`, `Procfile`)
2. เข้า https://render.com → New → Web Service → เชื่อม GitHub repo ที่สร้างไว้
3. ตั้งค่า:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. กด Deploy รอสักครู่ จะได้ลิงก์ประมาณ `https://your-app.onrender.com` ส่งลิงก์นี้ให้เพื่อนดูได้เลย

ทุกครั้งที่ push โค้ดใหม่ขึ้น GitHub (branch `main`) Render จะ build + deploy ให้อัตโนมัติ

### ทางเลือกอื่น
- **Railway** (railway.app) — ใช้ขั้นตอนคล้ายกัน
- **PythonAnywhere** — เหมาะกับแอป Flask เล็ก ๆ ฟรี
- **Replit** — สร้าง Repl แบบ Python/Flask, วางไฟล์เหล่านี้ แล้วกด Run + Deploy

## โครงสร้างไฟล์

```
app.py              โค้ดหลัก (Flask backend + หน้าเว็บ HTML/CSS/JS ฝังในไฟล์เดียว รวมข้อมูลทริปด้วย)
requirements.txt    Python dependencies
Procfile             สำหรับ deploy บน Render/Heroku-style platform
```

## จะเพิ่มสถานที่ทีหลังยังไง

บอกในแชทกับ Claude ได้เลยว่าจะเพิ่ม/แก้/ลบอะไร แล้วจะแก้ `DEFAULT_TRIP` ใน `app.py` พร้อม commit + push ให้อัตโนมัติ (Render จะ deploy ให้เองภายในไม่กี่นาที)
