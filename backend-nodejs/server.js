// server.js - Node.js Backend สำหรับระบบจัดการฟาร์ม

// 1. นำเข้าไลบรารีที่จำเป็น
const express = require('express'); // Express.js สำหรับสร้าง API
const admin = require('firebase-admin'); // Firebase Admin SDK
const cors = require('cors'); // CORS สำหรับอนุญาต Frontend เรียก Backend

// 2. Initialise Firebase Admin SDK
// คุณต้องเปลี่ยน "path/to/your/serviceAccountKey.json" ให้เป็น Path จริงๆ ของไฟล์ Service Account Key ของคุณ
// แนะนำ: วางไฟล์ serviceAccountKey.json ไว้ในโฟลเดอร์เดียวกับ server.js
let serviceAccount; // เปลี่ยนจาก var เป็น let เพื่อให้สอดคล้องกับ modern JS practices
try {
  serviceAccount = require("./serviceAccountKey.json"); // สมมติว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน
  // ตรวจสอบว่า serviceAccount เป็น Object ที่ถูกต้องหรือไม่ (อย่างน้อยต้องมี project_id)
  if (!serviceAccount || !serviceAccount.project_id) {
    throw new Error("Invalid serviceAccountKey.json file structure.");
  }
} catch (error) {
  console.error("Error loading serviceAccountKey.json:", error.message);
  console.error("Please ensure 'serviceAccountKey.json' is in the same directory as 'server.js' and is a valid JSON file.");
  console.error("You can download it from Firebase Console > Project settings > Service accounts > Generate new private key.");
  process.exit(1); // หยุดแอปพลิเคชันถ้าโหลดไฟล์ Service Account Key ไม่สำเร็จ
}

try {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
  console.log("Firebase Admin SDK initialized successfully.");
} catch (error) {
  console.error("Error initializing Firebase Admin SDK:", error);
  process.exit(1); // หยุดแอปพลิเคชันถ้า Firebase Init ไม่สำเร็จ
}

const db = admin.firestore(); // ดึง Firestore client
const auth = admin.auth(); // ดึง Firebase Authentication client

const app = express(); // สร้าง Express app
app.use(express.json()); // Middleware สำหรับอ่าน JSON body จาก Request
app.use(cors()); // ใช้ CORS Middleware เพื่ออนุญาตทุกโดเมน (สำหรับการพัฒนา)

// 3. API Endpoint สำหรับการสมัครสมาชิก (Register)
app.post('/api/register', async (req, res) => {
  const { email, password } = req.body; // ดึง email และ password จาก Request Body

  // ตรวจสอบข้อมูลเบื้องต้น
  if (!email || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }

  if (password.length < 6) {
    return res.status(400).json({ message: 'รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร' });
  }

  try {
    // 1. สร้างผู้ใช้ใหม่ใน Firebase Authentication
    const userRecord = await auth.createUser({
      email: email,
      password: password,
    });
    const uid = userRecord.uid; // ได้ User ID (UID) จาก Firebase Authentication

    // 2. เก็บข้อมูลผู้ใช้เพิ่มเติมใน Firestore
    // Collection 'Users' จะเก็บข้อมูลโปรไฟล์ผู้ใช้
    // Document ID จะใช้ UID ของผู้ใช้
    await db.collection('Users').doc(uid).set({
      email: email,
      role: 'member', // กำหนดบทบาทเริ่มต้นเป็น 'member'
      createdAt: admin.firestore.FieldValue.serverTimestamp() // บันทึกเวลาที่สร้าง
    });

    console.log(`User registered: ${email} (UID: ${uid})`);
    return res.status(200).json({ message: 'สมัครสมาชิกสำเร็จ', uid: uid });

  } catch (error) {
    console.error("Error during registration:", error);
    // จัดการข้อผิดพลาดที่อาจเกิดขึ้นจาก Firebase Authentication
    if (error.code === 'auth/email-already-exists') {
      return res.status(409).json({ message: 'อีเมลนี้ถูกใช้ไปแล้ว' });
    } else if (error.code === 'auth/invalid-password') {
      return res.status(400).json({ message: 'รหัสผ่านไม่ถูกต้องตามเงื่อนไข (ต้องมีอย่างน้อย 6 ตัวอักษร)' });
    } else {
      return res.status(500).json({ message: 'สมัครสมาชิกไม่สำเร็จ', error: error.message });
    }
  }
});

// 4. API Endpoint สำหรับการเข้าสู่ระบบ (Login)
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body; // ดึง email และ password จาก Request Body

  if (!email || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }

  try {
    // ใน Node.js Backend, การ Login โดยตรงด้วย email/password เพื่อรับ ID Token
    // มักจะทำบน Frontend โดยใช้ Firebase Client SDK
    // Backend จะรับ ID Token มา Verify อีกที
    // แต่สำหรับตัวอย่างนี้ เราจะจำลองการตรวจสอบผู้ใช้แบบง่ายๆ
    // ในโปรเจกต์จริง คุณอาจจะให้ Frontend ส่ง ID Token มาให้ Backend Verify
    // หรือ Backend จะสร้าง Custom Token ให้ Frontend ไป Login ด้วย

    // ตัวอย่างการตรวจสอบผู้ใช้ (อย่างง่ายๆ) - ไม่ได้ทำการ Login จริงๆ ด้วยรหัสผ่าน
    // ในโปรเจกต์จริงควรใช้ Firebase Client SDK บน Frontend เพื่อ Login
    // และส่ง ID Token ที่ได้มาให้ Backend Verify
    const userRecord = await auth.getUserByEmail(email);

    // ถ้ามาถึงตรงนี้ได้ แสดงว่าอีเมลมีอยู่ในระบบ (แต่ยังไม่ได้ตรวจสอบรหัสผ่าน)
    // ในการใช้งานจริง: Frontend จะต้องใช้ Firebase Client SDK เพื่อ signInWithEmailAndPassword
    // และส่ง ID Token ที่ได้มาให้ Backend เพื่อยืนยันตัวตนสำหรับการเรียก API อื่นๆ
    console.log(`User found for login: ${email} (UID: ${userRecord.uid})`);
    return res.status(200).json({ message: 'Login successful (Backend check only)', uid: userRecord.uid });

  } catch (error) {
    console.error("Error during login:", error);
    if (error.code === 'auth/user-not-found') {
      return res.status(401).json({ message: 'ไม่พบผู้ใช้นี้' });
    } else if (error.code === 'auth/wrong-password') {
      // Note: This error might not be directly caught here if Frontend handles actual sign-in
      return res.status(401).json({ message: 'รหัสผ่านไม่ถูกต้อง' });
    } else {
      return res.status(500).json({ message: 'เข้าสู่ระบบไม่สำเร็จ', error: error.message });
    }
  }
});

// 5. เริ่ม Server
const PORT = process.env.PORT || 5000; // กำหนด Port ให้ Server รัน
app.listen(PORT, () => {
  console.log(`Node.js Backend Server is running on port ${PORT}`);
  console.log(`Register API: http://localhost:${PORT}/api/register`);
  console.log(`Login API: http://localhost:${PORT}/api/login`);
});