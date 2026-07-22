# รีวิวโค้ด — app.py

รีวิวคร่าวๆ ของ `app.py` (Flask trip planner แบบดูอย่างเดียว)

ภาพรวม: โครงสร้างโค้ดสะอาดดี แบ่งสัดส่วนชัดเจน (Flask ฝั่งเดียว render ข้อมูล static เข้า template, JS แยกส่วน render/map/route) ปัญหาหลักที่พบไม่ใช่บั๊ก แต่เป็นเรื่อง privacy ของข้อมูลจริงที่ฝังอยู่ในซอร์สโค้ด

## 1. ข้อมูลส่วนตัวจะถูกเผยแพร่แบบสาธารณะ (สำคัญสุด)

README แนะนำให้ push ขึ้น GitHub repo แล้ว deploy บน Render พร้อมส่งลิงก์ให้เพื่อนดู แต่ `DEFAULT_TRIP` (app.py บรรทัด 23) มี:

- ที่อยู่คอนโดจริง (`คอนโด The President สาทร-ราชพฤกษ์ เฟส 3`)
- เลขไฟลท์จริง (FD 3235, DD 575)
- จำนวนผู้โดยสาร

ฝังอยู่ในซอร์สโค้ดตรงๆ ถ้า repo เป็น public หรือ Render URL ถูกแชร์ต่อ/เดาได้ ข้อมูลพวกนี้จะถูกเห็นโดยใครก็ได้ ไม่ใช่แค่ "เพื่อนที่ได้ลิงก์"

**คำแนะนำ:**
- ตั้ง GitHub repo เป็น **private** อย่างน้อยที่สุด
- ถ้าอยากกันคนที่ได้ลิงก์แบบสุ่ม/แชร์ผิดคน อาจเพิ่ม basic auth เบาๆ หรือ URL แบบเดายาก

## 2. พึ่ง public OSRM demo server

`fetchRoadRoute` (app.py บรรทัด 401) เรียก `router.project-osrm.org` ซึ่งเป็น demo server ฟรีที่ limit rate ต่ำ ไม่ได้ออกแบบมาสำหรับ production ถ้ามีคนเปิดพร้อมกันหลายคนหรือรีเฟรชถี่ๆ อาจโดน rate-limit จนเส้นทางไม่ขึ้น

มี fallback เป็นเส้นตรงอยู่แล้วใน catch block เลยยังพอโอเคในระดับ personal use แต่ควรรู้ข้อจำกัดนี้ไว้

## 3. ไม่มี integrity/SRI บน CDN resources

leaflet.js/css และ Google Fonts (app.py บรรทัด 159-163) โหลดจาก CDN โดยไม่มี `integrity` attribute ความเสี่ยงต่ำเพราะไม่มี user input ที่ต้อง sanitize จริงจัง แต่ถ้า CDN ถูกแฮ็คก็จะรัน JS แปลกปลอมได้ ใส่ `integrity` + `crossorigin` เพิ่มความมั่นใจได้

## จุดที่ตรวจแล้วไม่พบปัญหา

- `guessCategory` fallback logic
- `isDirectLeg` สำหรับ flight/ferry legs
- `escapeHtml` ใน render functions
- `trip | tojson` เข้า `<script>` tag (Flask/Jinja tojson filter escape ให้อัตโนมัติอยู่แล้ว)
