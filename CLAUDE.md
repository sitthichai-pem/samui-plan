# samui_plan

Flask trip planner แบบดูอย่างเดียว (single-page: แผนที่ + หมุด + ไทม์ไลน์รายวัน) — โค้ดทั้งหมดอยู่ใน `app.py` ไฟล์เดียว (Flask backend + HTML/CSS/JS ฝังในไฟล์)

## จะแก้แผนทริปยังไง

ไม่มีโหมดแก้ไขบนเว็บ แก้ได้ทางเดียวคือแก้ตัวแปร `DEFAULT_TRIP` ใน `app.py` โดยตรง

**หลังแก้ไขไฟล์ในโปรเจกต์นี้เสร็จทุกครั้ง ให้ commit + push ขึ้น `origin/main` ให้เลยโดยไม่ต้องถามก่อน** (ผู้ใช้ยืนยันไว้แล้วว่าต้องการแบบนี้เสมอ) เพราะ Render ผูก auto-deploy กับ push ขึ้น branch `main` อยู่แล้ว

## จุดที่ต้องระวังเสมอ (ดูรายละเอียดเต็มใน REVIEW.md)

- **ข้อมูลใน `DEFAULT_TRIP` เป็นข้อมูลจริงของผู้ใช้** (ที่อยู่คอนโด, เลขไฟลท์, จำนวนผู้โดยสาร) — README แนะนำให้ push repo นี้ขึ้น GitHub แล้ว deploy public บน Render พร้อมแชร์ลิงก์ ถ้า repo เป็น public ข้อมูลส่วนตัวเหล่านี้จะเผยแพร่ได้ ก่อนแนะนำให้ push/deploy ควรเตือนเรื่อง private repo หรือการป้องกันลิงก์ก่อนทุกครั้ง
- routing เส้นทาง (`fetchRoadRoute`) พึ่ง public OSRM demo server (`router.project-osrm.org`) — ไม่เหมาะกับ production traffic สูง มี fallback เป็นเส้นตรงอยู่แล้ว
- CDN resources (leaflet, Google Fonts) ไม่มี SRI/`integrity` attribute
