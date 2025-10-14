import tkinter as tk
from tkinter import messagebox
from firebase_config import db
from utils import add_log
from datetime import datetime
import pytz

class AddPlantScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Add New Plant", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=10)

        # ช่องกรอกข้อมูล
        tk.Label(self.frame, text="Name", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.name_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.name_entry.pack(pady=5)

        tk.Label(self.frame, text="Type", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.type_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.type_entry.pack(pady=5)

        tk.Label(self.frame, text="Quantity", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.quantity_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.quantity_entry.pack(pady=5)

        tk.Label(self.frame, text="Last Watered (YYYY-MM-DD)", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.last_watered_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.last_watered_entry.pack(pady=5)

        # ปุ่ม Add
        add_btn = tk.Button(self.frame, text="✅ Add Plant", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", relief="flat", width=20, command=self.add_plant)
        add_btn.pack(pady=20)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#27ae60"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#2ecc71"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

    def add_plant(self):
        name = self.name_entry.get()
        type_ = self.type_entry.get()
        quantity = self.quantity_entry.get()
        last_watered = self.last_watered_entry.get()

        if not name or not type_ or not quantity:
            messagebox.showwarning("Warning", "Please fill in all required fields.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        user_id = self.app.current_user['localId']
        try:
            plant_data = {
                "name": name,
                "type": type_,
                "quantity": quantity,
                "last_watered": last_watered or "Not Set",
                "added_by": user_id
            }
            plant_id = db.child("farms").child(self.app.current_farm).child("plants").push(plant_data)["name"]
            add_log(self.app.current_farm, user_id, "added_plant", plant_data)
            messagebox.showinfo("Success", "Plant added successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add plant: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        from screens.plant_screen import PlantScreen
        PlantScreen(self.app)