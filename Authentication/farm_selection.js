// farm_selection.js - JavaScript Logic สำหรับหน้าเลือกฟาร์ม (farm_selection.html)

// Import Firebase Authentication modules
import { getAuth, signOut } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js';
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js';

// ***********************************************************************************
// สำคัญ: สำหรับการรันบนเครื่องของคุณเอง (Localhost) คุณต้องใส่ Firebase Config ของคุณที่นี่
//
// นี่คือค่าสำหรับ Firebase CLIENT SDK (สำหรับ Frontend)
// ไม่ใช่ไฟล์ serviceAccountKey.json (ซึ่งใช้สำหรับ Backend เท่านั้นและต้องเก็บเป็นความลับ)
//
// วิธีหาค่านี้:
// 1. เข้าสู่ระบบ Firebase Console ของโปรเจกต์คุณ
// 2. ไปที่ Project settings (ไอคอนฟันเฟือง) -> General
// 3. เลื่อนลงมาที่ "Your apps" แล้วเลือก "Web" (ไอคอน </>)
// 4. คัดลอก Object ที่ชื่อว่า "firebaseConfig" มาวางแทนที่ด้านล่างนี้
// ***********************************************************************************
const firebaseConfig = {
    apiKey: "AIzaSyCHOMHm_XTE1_-oZVloRudi7Fxhs2Ygu_U",
    authDomain: "my-small-farm-system.firebaseapp.com",
    projectId: "my-small-farm-system",
    storageBucket: "my-small-farm-system.firebasestorage.app",
    messagingSenderId: "214056545877",
    appId: "1:214056545877:web:ff1b28273d8f65e70c2edc"
};

// ตรวจสอบว่า Firebase Config ถูกต้องหรือไม่
if (!firebaseConfig.apiKey || !firebaseConfig.authDomain || !firebaseConfig.projectId) {
    console.error("Firebase configuration is incomplete or incorrect. Please update firebaseConfig in farm_selection.js.");
    alert("Firebase configuration error. Please check the console for details.");
    // หาก config ไม่ถูกต้อง เราจะไม่เริ่มต้น Firebase เพื่อป้องกัน Error เพิ่มเติม
    throw new Error("Firebase configuration is missing or invalid.");
}

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

let selectedFarmId = null;
const farmCards = document.querySelectorAll('.farm-card');
const nextButton = document.getElementById('nextButton');
const logoutButton = document.getElementById('logoutButton');

// Function to handle farm card selection
farmCards.forEach(card => {
    card.addEventListener('click', () => {
        // Remove 'selected' class from all cards
        farmCards.forEach(c => c.classList.remove('selected'));
        // Add 'selected' class to the clicked card
        card.classList.add('selected');
        selectedFarmId = card.dataset.farmId; // Get farm ID from data-farm-id attribute
        nextButton.disabled = false; // Enable the Next button
    });
});

// Event listener for the Next button
nextButton.addEventListener('click', () => {
    if (selectedFarmId) {
        console.log('Selected Farm ID:', selectedFarmId);
        // In a real application, you would save this selection
        // and redirect to a dashboard specific to this farm.
        // For now, let's just show an alert and redirect to a placeholder.
        alert(`คุณได้เลือก ${selectedFarmId} แล้ว!`);
        // Placeholder redirect: Replace with your actual dashboard page
        window.location.href = 'dashboard.html?farm=' + selectedFarmId;
    } else {
        alert('กรุณาเลือกฟาร์มก่อนดำเนินการต่อ');
    }
});

// Event listener for the Logout button
logoutButton.addEventListener('click', async () => {
    try {
        await signOut(auth);
        alert('ออกจากระบบสำเร็จ');
        window.location.href = 'index.html'; // Redirect to login page
    } catch (error) {
        console.error('Error signing out:', error);
        alert('เกิดข้อผิดพลาดในการออกจากระบบ: ' + error.message);
    }
});

// Basic authentication check (optional, but good practice)
// Redirect to login if user is not authenticated
auth.onAuthStateChanged(user => {
    if (!user) {
        // If no user is logged in, redirect to the login page
        window.location.href = 'index.html';
    }
});