# วางแพลนเที่ยว — Flask Trip Planner

เว็บแอปวางแผนทริปหน้าเดียว: แผนที่ + ปักหมุด + ไทม์ไลน์รายวัน
คุณ (เจ้าของ) แก้ไขได้ผ่านรหัสผ่าน ส่วนคนอื่นที่เปิดลิงก์เว็บนี้จะเห็นแบบ **ดูอย่างเดียว**

ข้อมูลทริปตอนนี้ตั้งต้นไว้ให้แล้ว: เริ่มจากคอนโด The President สาทร-ราชพฤกษ์ เฟส 3 → สนามบินดอนเมือง (เที่ยวบิน FD 3235) → เช็คอิน COSI Samui Chaweng Beach (วันที่ 1) และเช็คเอาต์ + เที่ยวบิน DD 575 กลับ (วันที่ 4) ส่วนวันที่ 2-3 เว้นว่างไว้ให้ปักหมุดเพิ่มเอง

## รหัสผ่านแก้ไข (สำคัญ — เปลี่ยนก่อน deploy จริง!)

รหัสผ่านเริ่มต้นอยู่ในไฟล์ `app.py` ตัวแปร `DEFAULT_TRIP["passcode"]` (ค่าเริ่มต้นคือ `changeme123`)
**เปลี่ยนเป็นรหัสของคุณเองก่อน deploy** ไม่งั้นใครก็ปลดล็อกโหมดแก้ไขได้

ถ้าเคย deploy ไปแล้วและมีไฟล์ `trip_data.json` เกิดขึ้นแล้ว การแก้ `DEFAULT_TRIP` ใน `app.py` จะไม่มีผล (เพราะแอปอ่านจาก `trip_data.json` ก่อน) — ให้แก้รหัสผ่านในไฟล์ `trip_data.json` โดยตรงแทน หรือลบไฟล์นั้นทิ้งแล้วรันใหม่

## รันทดสอบในเครื่องตัวเอง

```bash
pip install -r requirements.txt
python app.py
```

เปิด http://localhost:5000 — ครั้งแรกจะสร้างไฟล์ `trip_data.json` ให้อัตโนมัติ

## Deploy ให้คนอื่นเข้าดูได้ (แนะนำ: Render.com — ฟรี)

1. สร้าง repo บน GitHub แล้วอัปโหลดไฟล์ทั้งหมดในโฟลเดอร์นี้ (`app.py`, `requirements.txt`, `Procfile`)
2. เข้า https://render.com → New → Web Service → เชื่อม GitHub repo ที่สร้างไว้
3. ตั้งค่า:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. เพิ่ม Environment Variable ชื่อ `SECRET_KEY` เป็นข้อความสุ่มยาวๆ ของตัวเอง (สำคัญ ไม่งั้น session ผู้ใช้จะหลุดทุกครั้งที่เซิร์ฟเวอร์รีสตาร์ท)
5. กด Deploy รอสักครู่ จะได้ลิงก์ประมาณ `https://your-app.onrender.com` ส่งลิงก์นี้ให้เพื่อนดูได้เลย

**หมายเหตุเรื่องข้อมูล**: Render แบบฟรีไม่มี persistent disk ถ้าเซิร์ฟเวอร์ restart ข้อมูลใน `trip_data.json` อาจหายกลับไปเป็นค่าเริ่มต้น ถ้าอยากให้ข้อมูลอยู่ถาวรจริง ๆ ให้เพิ่ม Render Disk (มีในแผนเสียเงิน) หรือย้ายไปเก็บใน database ฟรีอย่าง Render PostgreSQL / Supabase — บอกได้ถ้าอยากให้ช่วยต่อ

### ทางเลือกอื่น
- **Railway** (railway.app) — ใช้ขั้นตอนคล้ายกัน มี persistent volume แบบฟรีเล็กน้อย
- **PythonAnywhere** — เหมาะกับแอป Flask เล็ก ๆ ฟรี มี disk ถาวร
- **Replit** — สร้าง Repl แบบ Python/Flask, วางไฟล์เหล่านี้ แล้วกด Run + Deploy

## โครงสร้างไฟล์

```
app.py              โค้ดหลัก (Flask backend + หน้าเว็บ HTML/CSS/JS ฝังในไฟล์เดียว)
requirements.txt    Python dependencies
Procfile             สำหรับ deploy บน Render/Heroku-style platform
trip_data.json       (สร้างอัตโนมัติตอนรันครั้งแรก) เก็บข้อมูลทริปจริง
```

## จะเพิ่มสถานที่ทีหลังยังไง

- **ผ่านเว็บ**: ปลดล็อกโหมดแก้ไขด้วยรหัสผ่าน แล้วคลิกบนแผนที่เพื่อปักหมุดได้เลย
- **บอกในแชทนี้**: บอกชื่อสถานที่มา แล้วให้ช่วยแก้ `DEFAULT_TRIP` ในโค้ดหรือแก้ `trip_data.json` ให้ตรงตำแหน่งจริงบนแผนที่
