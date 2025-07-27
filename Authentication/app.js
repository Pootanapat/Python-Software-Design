// app.js - ไฟล์ JavaScript สำหรับจัดการ Logic ของหน้า Login

// Import Firebase Authentication modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js';
import { getAuth, signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js';

// Firebase Client-side Configuration (จากรูปภาพที่คุณส่งมา)
// คุณต้องแน่ใจว่าค่าเหล่านี้ถูกต้องและมาจาก Firebase Console ของคุณ
const firebaseConfig = {
    apiKey: "AIzaSyCHOMHm_XTE1_-oZVloRudi7Fxhs2Ygu_U",
    authDomain: "my-small-farm-system.firebaseapp.com",
    projectId: "my-small-farm-system",
    storageBucket: "my-small-farm-system.firebasestorage.app",
    messagingSenderId: "214056545877",
    appId: "1:214056545877:web:ff1b28273d8f65e70c2edc"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerLink = document.getElementById('registerLink');
    const forgotPasswordLink = document.querySelector('a[href="#"]'); // ลิงก์ลืมรหัสผ่าน

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // ป้องกันการ Submit ฟอร์มแบบปกติ

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            // ตรวจสอบข้อมูลเบื้องต้น (Validation)
            if (!email || !password) {
                alert('กรุณากรอกอีเมลและรหัสผ่านให้ครบถ้วน');
                return;
            }

            try {
                // 1. ส่งข้อมูลไปที่ Backend Node.js เพื่อยืนยันตัวตน (Backend จะตรวจสอบว่า Email มีอยู่ในระบบหรือไม่)
                const backendResponse = await fetch('http://localhost:5000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const backendData = await backendResponse.json();

                if (backendResponse.ok) {
                    // 2. ถ้า Backend ยืนยันสำเร็จ (ว่า Email มีอยู่) ให้ทำการ Login ด้วย Firebase Client SDK บน Frontend
                    //    เพื่อให้ Firebase Client SDK สร้าง Session และจัดการสถานะผู้ใช้
                    await signInWithEmailAndPassword(auth, email, password); // เรียกใช้ signInWithEmailAndPassword โดยตรงจาก auth

                    alert('เข้าสู่ระบบสำเร็จ!');
                    // เปลี่ยนเส้นทางไปยังหน้าเลือกฟาร์ม
                    window.location.href = 'farm_selection.html';
                } else {
                    // Login ไม่สำเร็จจาก Backend (เช่น Email ไม่ถูกต้อง)
                    alert('เข้าสู่ระบบไม่สำเร็จ: ' + (backendData.message || 'เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุจาก Backend'));
                }
            } catch (error) {
                console.error('Error during login:', error);
                // ตรวจสอบ Error จาก Firebase Client SDK หรือ Network ด้วย
                if (error.code && error.code.startsWith('auth/')) {
                    // Error จาก Firebase Authentication (เช่น รหัสผ่านผิด, ผู้ใช้ไม่พบ)
                    alert('เข้าสู่ระบบไม่สำเร็จ: ' + error.message);
                } else {
                    // Error ในการเชื่อมต่อกับ Backend หรืออื่นๆ
                    alert('ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาลองใหม่อีกครั้ง หรือตรวจสอบว่า Backend ทำงานอยู่');
                }
            }
        });
    }

    if (registerLink) {
        registerLink.addEventListener('click', (e) => {
            e.preventDefault(); // ป้องกันการเปลี่ยนหน้าแบบปกติ
            window.location.href = 'register.html'; // เปลี่ยนเส้นทางไปหน้าสมัครสมาชิก
        });
    }

    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault(); // หยุดการเปลี่ยนเส้นทางแบบปกติ
            alert('ฟังก์ชันลืมรหัสผ่านยังไม่ได้ถูกนำมาใช้งาน');
        });
    }
});