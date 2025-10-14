import tkinter as tk
from tkinter import messagebox
from utils import get_user_role, check_permission
from firebase_config import db

class FarmDashboardScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # ดึงชื่อฟาร์มจาก Firebase
        farm_id = self.app.current_farm
        farm_name = db.child("farms").child(farm_id).child("name").get().val()

        # แสดงชื่อฟาร์ม (ขนาดเล็ก)
        farm_label = tk.Label(self.frame, text=f"Farm: {farm_name}", font=("Arial", 10), bg="#f5f5f5", fg="#7f8c8d")
        farm_label.pack(pady=(20, 5))

        # แสดงตำแหน่งของผู้ใช้
        user_id = self.app.current_user['localId']
        role = get_user_role(user_id, farm_id)
        position_label = tk.Label(self.frame, text=f"Position: {role or 'No Role'}", font=("Arial", 10, "italic"), bg="#f5f5f5", fg="#2c3e50")
        position_label.pack(pady=5)

        # ปุ่ม Animals (แสดงถ้าสามารถดูได้)
        if check_permission(user_id, farm_id, "view"):
            animals_btn = tk.Button(self.frame, text="🐾 Animals", font=("Arial", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=15, height=2, command=self.go_to_animals)
            animals_btn.pack(pady=5)
            animals_btn.bind("<Enter>", lambda e: animals_btn.config(bg="#2980b9"))
            animals_btn.bind("<Leave>", lambda e: animals_btn.config(bg="#3498db"))

        # ปุ่ม Plants (แสดงถ้าสามารถดูได้)
        if check_permission(user_id, farm_id, "view"):
            plants_btn = tk.Button(self.frame, text="🌱 Plants", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", relief="flat", width=15, height=2, command=self.go_to_plants)
            plants_btn.pack(pady=5)
            plants_btn.bind("<Enter>", lambda e: plants_btn.config(bg="#27ae60"))
            plants_btn.bind("<Leave>", lambda e: plants_btn.config(bg="#2ecc71"))

        # ปุ่ม Farm Manager (เฉพาะเจ้าของหรือผู้มีสิทธิ์)
        if check_permission(user_id, farm_id, "manage_members"):
            manager_btn = tk.Button(self.frame, text="📊 Farm Manager", font=("Arial", 12, "bold"), bg="#9b59b6", fg="white", relief="flat", width=15, height=2, command=self.go_to_manager)
            manager_btn.pack(pady=5)
            manager_btn.bind("<Enter>", lambda e: manager_btn.config(bg="#8e44ad"))
            manager_btn.bind("<Leave>", lambda e: manager_btn.config(bg="#9b59b6"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#c0392b"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#e74c3c"))

    def go_to_animals(self):
        self.app.clear_window()
        from screens.animal_screen import AnimalScreen
        AnimalScreen(self.app)

    def go_to_plants(self):
        self.app.clear_window()
        from screens.plant_screen import PlantScreen
        PlantScreen(self.app)

    def go_to_manager(self):
        self.app.clear_window()
        from screens.manager_screen import ManagerScreen
        ManagerScreen(self.app)

    def go_back(self):
        self.app.clear_window()
        from screens.farm_selection_screen import FarmSelectionScreen
        FarmSelectionScreen(self.app)