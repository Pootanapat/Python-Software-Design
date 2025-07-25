// app.js - ไฟล์ JavaScript สำหรับจัดการ Logic ของหน้า Login

// 1. ดึง Element ต่างๆ ที่จำเป็นจาก HTML
const loginForm = document.getElementById('loginForm'); // ฟอร์ม Login ทั้งหมด
const emailInput = document.getElementById('email');   // ช่องกรอกอีเมล
const passwordInput = document.getElementById('password'); // ช่องกรอกรหัสผ่าน
const rememberMeCheckbox = document.getElementById('rememberMe'); // Checkbox จดจำฉัน
const registerLink = document.getElementById('registerLink'); // ลิงก์สมัครสมาชิก
const forgotPasswordLink = document.querySelector('a[href="#"]'); // ลิงก์ลืมรหัสผ่าน

// 2. เพิ่ม Event Listener สำหรับการกดปุ่ม "เข้าสู่ระบบ"
//    เมื่อผู้ใช้กดปุ่ม submit ในฟอร์ม loginForm, ฟังก์ชัน async นี้จะทำงาน
loginForm.addEventListener('submit', async function(event) {
    event.preventDefault(); // สำคัญมาก! หยุดการทำงานปกติของฟอร์ม (ไม่ให้รีเฟรชหน้า)

    // ดึงค่าที่ผู้ใช้กรอกเข้ามา
    const email = emailInput.value.trim(); // .trim() ใช้ลบช่องว่างหน้า/หลัง
    const password = passwordInput.value.trim();
    const rememberMe = rememberMeCheckbox.checked; // true หรือ false

    // ตรวจสอบข้อมูลเบื้องต้น (Validation)
    if (!email || !password) {
        alert('กรุณากรอกอีเมลและรหัสผ่านให้ครบถ้วน');
        return; // หยุดการทำงานถ้าข้อมูลไม่ครบ
    }

    console.log('--- ข้อมูลเข้าสู่ระบบที่ได้รับ ---');
    console.log('อีเมล:', email);
    console.log('รหัสผ่าน:', password); // ในโปรเจกต์จริง ไม่ควร console.log รหัสผ่านใน Production
    console.log('จดจำฉัน:', rememberMe);

    // *******************************************************************
    // 3. ส่วนสำคัญ: เรียก Backend API เพื่อทำการ Login
    //    ตรงนี้คือจุดที่ Frontend (JavaScript) จะส่งข้อมูลไปให้ Backend (Python)
    //    Backend Developer จะต้องสร้าง API Endpoint สำหรับการ Login
    // *******************************************************************
    try {
        // ตัวอย่างการใช้ fetch API เพื่อส่งข้อมูลไป Backend
        // สมมติว่า Backend ของเราทำงานอยู่ที่ http://localhost:5000
        // และมี API สำหรับ Login ที่ /api/login
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST', // ใช้เมธอด POST สำหรับการส่งข้อมูล Login
            headers: {
                'Content-Type': 'application/json' // บอก Backend ว่าข้อมูลที่เราส่งไปเป็น JSON
            },
            body: JSON.stringify({ email: email, password: password }) // แปลงข้อมูลเป็น JSON String
        });

        const data = await response.json(); // รอรับข้อมูลตอบกลับจาก Backend และแปลงเป็น JSON

        // ตรวจสอบผลลัพธ์จาก Backend
        if (response.ok) { // ถ้า Backend ตอบกลับมาด้วยสถานะ 2xx (เช่น 200 OK)
            alert('เข้าสู่ระบบสำเร็จ! ยินดีต้อนรับ ' + email);
            console.log('การตอบกลับจาก Backend (สำเร็จ):', data);

            // *******************************************************************
            // 4. จัดการหลัง Login สำเร็จ
            //    - Backend อาจจะส่ง Firebase ID Token หรือข้อมูลผู้ใช้กลับมา
            //    - คุณอาจจะเก็บ Token นี้ไว้ใน localStorage หรือ sessionStorage เพื่อใช้ในการเรียก API อื่นๆ
            //    - จากนั้นเปลี่ยนเส้นทางผู้ใช้ไปยังหน้าถัดไป (เช่น หน้าเลือกฟาร์ม)
            // *******************************************************************
            // ตัวอย่าง: เปลี่ยนเส้นทางไปยังหน้าเลือกฟาร์ม (สมมติว่ามีไฟล์ชื่อ farm_selection.html)
            // window.location.href = 'farm_selection.html';

        } else { // ถ้า Backend ตอบกลับมาด้วยสถานะ Error (เช่น 400 Bad Request, 401 Unauthorized)
            alert('เข้าสู่ระบบไม่สำเร็จ: ' + (data.message || 'เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ'));
            console.error('การตอบกลับจาก Backend (ข้อผิดพลาด):', data);
        }
    } catch (error) {
        // จัดการข้อผิดพลาดในการเชื่อมต่อ (เช่น Backend ไม่ได้รันอยู่ หรือ Network มีปัญหา)
        console.error('เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์:', error);
        alert('ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาลองใหม่อีกครั้ง หรือตรวจสอบว่า Backend ทำงานอยู่');
    }
});

// 5. เพิ่ม Event Listener สำหรับลิงก์ "สมัครสมาชิก"
registerLink.addEventListener('click', function(event) {
    event.preventDefault(); // หยุดการเปลี่ยนเส้นทางแบบปกติ

    // เปลี่ยนเส้นทางไปยังหน้าสมัครสมาชิก (register.html)
    // บรรทัดนี้คือตัวที่ควรจะพาไปหน้าใหม่
    window.location.href = 'register.html';
});

// 6. เพิ่ม Event Listener สำหรับลิงก์ "ลืมรหัสผ่าน?"
//    เราใช้ querySelector เพราะมันอาจจะเป็นลิงก์แรกที่มี href="#"
if (forgotPasswordLink) { // ตรวจสอบว่าลิงก์มีอยู่จริง
    forgotPasswordLink.addEventListener('click', function(event) {
        event.preventDefault(); // หยุดการเปลี่ยนเส้นทางแบบปกติ

        alert('ฟังก์ชันลืมรหัสผ่านยังไม่ได้ถูกนำมาใช้งาน');
        // *******************************************************************
        // ในโปรเจกต์จริง:
        // - คุณจะต้องสร้างหน้าสำหรับรีเซ็ตรหัสผ่าน
        // - และใช้ Firebase Authentication สำหรับการส่งอีเมลรีเซ็ต
        // *******************************************************************
        // window.location.href = 'forgot_password.html';
    });
}
// app.js - สำหรับหน้า Login (index.html)
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerLink = document.getElementById('registerLink');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // ป้องกันการ Submit ฟอร์มแบบปกติ

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // ส่งข้อมูลไปที่ Backend Node.js
                const response = await fetch('http://localhost:5000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Login สำเร็จ
                    alert('เข้าสู่ระบบสำเร็จ!');
                    // เปลี่ยนเส้นทางไปยังหน้าเลือกฟาร์ม
                    window.location.href = 'farm_selection.html'; // <--- เปลี่ยนตรงนี้
                } else {
                    // Login ไม่สำเร็จ
                    alert('เข้าสู่ระบบไม่สำเร็จ: ' + data.message);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาลองใหม่อีกครั้ง หรือตรวจสอบว่า Backend ทำงานอยู่');
            }
        });
    }

    if (registerLink) {
        registerLink.addEventListener('click', (e) => {
            e.preventDefault(); // ป้องกันการเปลี่ยนหน้าแบบปกติ
            window.location.href = 'register.html'; // เปลี่ยนเส้นทางไปหน้าสมัครสมาชิก
        });
    }
});
