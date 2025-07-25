// register.js - ไฟล์ JavaScript สำหรับจัดการ Logic ของหน้าสมัครสมาชิก

// 1. ดึง Element ต่างๆ ที่จำเป็นจาก HTML
const registerForm = document.getElementById('registerForm'); // ฟอร์มสมัครสมาชิกทั้งหมด
const registerEmailInput = document.getElementById('registerEmail'); // ช่องกรอกอีเมล
const registerPasswordInput = document.getElementById('registerPassword'); // ช่องกรอกรหัสผ่าน
const confirmPasswordInput = document.getElementById('confirmPassword'); // ช่องยืนยันรหัสผ่าน
const loginLink = document.getElementById('loginLink'); // ลิงก์เข้าสู่ระบบ

// 2. เพิ่ม Event Listener สำหรับการกดปุ่ม "สมัครสมาชิก"
//    เมื่อผู้ใช้กดปุ่ม submit ในฟอร์ม registerForm, ฟังก์ชัน async นี้จะทำงาน
registerForm.addEventListener('submit', async function(event) {
    event.preventDefault(); // สำคัญมาก! หยุดการทำงานปกติของฟอร์ม (ไม่ให้รีเฟรชหน้า)

    // ดึงค่าที่ผู้ใช้กรอกเข้ามา
    const email = registerEmailInput.value.trim();
    const password = registerPasswordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    // ตรวจสอบข้อมูลเบื้องต้น (Validation)
    if (!email || !password || !confirmPassword) {
        alert('กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง');
        return;
    }

    if (password !== confirmPassword) {
        alert('รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน');
        return;
    }

    if (password.length < 6) {
        alert('รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร');
        return;
    }

    console.log('--- ข้อมูลสมัครสมาชิกที่ได้รับ ---');
    console.log('อีเมล:', email);
    console.log('รหัสผ่าน:', password); // ในโปรเจกต์จริง ไม่ควร console.log รหัสผ่านใน Production

    // *******************************************************************
    // 3. ส่วนสำคัญ: เรียก Backend API เพื่อทำการสมัครสมาชิก
    //    ตรงนี้คือจุดที่ Frontend (JavaScript) จะส่งข้อมูลไปให้ Backend (Python)
    //    Backend Developer จะต้องสร้าง API Endpoint สำหรับการสมัครสมาชิก
    // *******************************************************************
    try {
        // ตัวอย่างการใช้ fetch API เพื่อส่งข้อมูลไป Backend
        // สมมติว่า Backend ของเราทำงานอยู่ที่ http://localhost:5000
        // และมี API สำหรับสมัครสมาชิกที่ /api/register
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST', // ใช้เมธอด POST สำหรับการส่งข้อมูลสมัครสมาชิก
            headers: {
                'Content-Type': 'application/json' // บอก Backend ว่าข้อมูลที่เราส่งไปเป็น JSON
            },
            body: JSON.stringify({ email: email, password: password }) // แปลงข้อมูลเป็น JSON String
        });

        const data = await response.json(); // รอรับข้อมูลตอบกลับจาก Backend และแปลงเป็น JSON

        // ตรวจสอบผลลัพธ์จาก Backend
        if (response.ok) { // ถ้า Backend ตอบกลับมาด้วยสถานะ 2xx (เช่น 200 OK)
            alert('สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ ' + email + '\nคุณสามารถเข้าสู่ระบบได้แล้ว');
            console.log('การตอบกลับจาก Backend (สำเร็จ):', data);

            // *******************************************************************
            // 4. จัดการหลังสมัครสมาชิกสำเร็จ
            //    - Backend อาจจะส่งข้อมูลผู้ใช้ที่สร้างใหม่กลับมา
            //    - จากนั้นเปลี่ยนเส้นทางผู้ใช้กลับไปยังหน้า Login
            // *******************************************************************
            window.location.href = 'index.html'; // พาผู้ใช้กลับไปหน้า Login

        } else { // ถ้า Backend ตอบกลับมาด้วยสถานะ Error (เช่น 400 Bad Request, 409 Conflict)
            alert('สมัครสมาชิกไม่สำเร็จ: ' + (data.message || 'เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ'));
            console.error('การตอบกลับจาก Backend (ข้อผิดพลาด):', data);
        }
    } catch (error) {
        // จัดการข้อผิดพลาดในการเชื่อมต่อ (เช่น Backend ไม่ได้รันอยู่ หรือ Network มีปัญหา)
        console.error('เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์:', error);
        alert('ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาลองใหม่อีกครั้ง หรือตรวจสอบว่า Backend ทำงานอยู่');
    }
});

// 5. เพิ่ม Event Listener สำหรับลิงก์ "เข้าสู่ระบบ"
loginLink.addEventListener('click', function(event) {
    // เนื่องจาก href="index.html" อยู่แล้ว เราไม่จำเป็นต้อง event.preventDefault()
    // แต่ถ้าใช้เป็น href="#" แล้วจัดการด้วย JS ก็ต้องใส่ event.preventDefault()
    // ในกรณีนี้ เราให้มันทำงานตาม href ปกติ
    console.log('กำลังเปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ...');
});
// register.js - สำหรับหน้าสมัครสมาชิก (register.html)
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginLink = document.getElementById('loginLink');

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // ป้องกันการ Submit ฟอร์มแบบปกติ

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            if (password !== confirmPassword) {
                alert('รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน');
                return;
            }

            try {
                // ส่งข้อมูลไปที่ Backend Node.js
                const response = await fetch('http://localhost:5000/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    // สมัครสมาชิกสำเร็จ
                    alert('สมัครสมาชิกสำเร็จ!');
                    // เปลี่ยนเส้นทางกลับไปหน้า Login
                    window.location.href = 'index.html'; // <--- เปลี่ยนตรงนี้
                } else {
                    // สมัครสมาชิกไม่สำเร็จ
                    alert('สมัครสมาชิกไม่สำเร็จ: ' + data.message);
                }
            } catch (error) {
                console.error('Error during registration:', error);
                alert('ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาลองใหม่อีกครั้ง หรือตรวจสอบว่า Backend ทำงานอยู่');
            }
        });
    }

    if (loginLink) {
        loginLink.addEventListener('click', (e) => {
            e.preventDefault(); // ป้องกันการเปลี่ยนหน้าแบบปกติ
            window.location.href = 'index.html'; // เปลี่ยนเส้นทางไปหน้า Login
        });
    }
});
