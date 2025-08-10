# คู่มือการใช้งาน Git สำหรับแต่ละ Branch

โปรเจกต์นี้ถูกแบ่งออกเป็นหลาย Branch ตามชื่อของแต่ละคน เพื่อให้ทำงานแยกกันอย่างอิสระ  
ห้ามแก้ไขไฟล์ใน Branch ของคนอื่น และควรทำงานเฉพาะใน Branch ของตัวเองเท่านั้น

## รายชื่อ Branch และผู้รับผิดชอบ
| Branch | ผู้ดูแล |
|--------|---------|
| `VEAR` | Vear |
| `FOTO` | Foto |
| `GUN`  | Gun |
| `SUN`  | Sun |
| `ICE`  | Ice |
| `MEJI` | Meji |
| `INK`  | Ink |

---

## ขั้นตอนการทำงาน

### 1. ตรวจสอบว่าอยู่ใน Branch ของตัวเอง
```bash
git branch
```
ถ้าไม่ได้อยู่ใน Branch ของตัวเอง ให้สลับไปก่อน เช่น:
```bash
git checkout ICE    # เปลี่ยน ICE เป็น branch ของคุณ
```

---

### 2. ดึงโค้ดล่าสุดของ Branch ตัวเอง
```bash
git pull origin ICE   # เปลี่ยน ICE เป็น branch ของคุณ
```

---

### 3. เพิ่มไฟล์ใหม่หรือแก้ไขไฟล์
เพิ่มไฟล์เข้า staging:
```bash
git add .
```
หรือเพิ่มเฉพาะไฟล์:
```bash
git add ชื่อไฟล์
```

---

### 4. Commit โค้ด
```bash
git commit -m "คำอธิบายสิ่งที่แก้ไข"
```

---

### 5. Push โค้ดขึ้น GitHub
```bash
git push origin ICE   # เปลี่ยน ICE เป็น branch ของคุณ
```

---

## ตัวอย่างการทำงานเต็มขั้นตอน (สำหรับ ICE)
```bash
git checkout ICE
git pull origin ICE
# แก้ไขไฟล์ หรือ เพิ่มไฟล์ใหม่
git add .
git commit -m "เพิ่มหน้า dashboard"
git push origin ICE
```

---

## ข้อควรระวัง
- ห้ามทำงานใน `main` หรือ Branch ของคนอื่น
- ก่อนเริ่มงานใหม่ทุกครั้ง ควร `git pull` branch ของตัวเองก่อน
- Commit message ควรบอกสิ่งที่ทำอย่างชัดเจน