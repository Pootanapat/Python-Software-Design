import tkinter as tk
from tkinter import messagebox, ttk
from firebase_config import db
from utils import check_permission
from datetime import datetime
import pytz

class PlantScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Plants in Farm", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=10)

        # ปุ่ม Add Plant (แสดงถ้ามีสิทธิ์)
        user_id = self.app.current_user['localId']
        if check_permission(user_id, self.app.current_farm, "edit_plant"):
            add_btn = tk.Button(self.frame, text="➕ Add Plant", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", relief="flat", width=15, command=self.go_to_add)
            add_btn.pack(pady=5)
            add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#27ae60"))
            add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#2ecc71"))

        # สร้าง Treeview สำหรับแสดงตาราง
        columns = ("name", "type", "quantity", "last_watered")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=8)
        
        # กำหนดหัวคอลัมน์
        self.tree.heading("name", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("last_watered", text="Last Watered")

        # กำหนดความกว้างของคอลัมน์
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("type", width=150, anchor="w")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("last_watered", width=180, anchor="w")

        # ใส่ Treeview ลงในหน้าจอ
        self.tree.pack(pady=10, fill="x", padx=20)

        # ปุ่ม Water Selected (แสดงถ้ามีสิทธิ์)
        if check_permission(user_id, self.app.current_farm, "edit_plant"):
            water_btn = tk.Button(self.frame, text="💧 Water Selected", font=("Arial", 10, "bold"), bg="#f39c12", fg="white", relief="flat", width=15, command=self.water_selected)
            water_btn.pack(pady=5)
            water_btn.bind("<Enter>", lambda e: water_btn.config(bg="#d35400"))
            water_btn.bind("<Leave>", lambda e: water_btn.config(bg="#f39c12"))

        # ปุ่ม Edit และ Delete (แสดงถ้ามีสิทธิ์)
        if check_permission(user_id, self.app.current_farm, "edit_plant"):
            edit_btn = tk.Button(self.frame, text="✏️ Edit Selected", font=("Arial", 10, "bold"), bg="#f39c12", fg="white", relief="flat", width=15, command=self.edit_selected)
            edit_btn.pack(pady=5)
            edit_btn.bind("<Enter>", lambda e: edit_btn.config(bg="#d35400"))
            edit_btn.bind("<Leave>", lambda e: edit_btn.config(bg="#f39c12"))

            delete_btn = tk.Button(self.frame, text="🗑️ Delete Selected", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", width=15, command=self.delete_selected)
            delete_btn.pack(pady=5)
            delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#c0392b"))
            delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#e74c3c"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

        self.load_plants()

    def load_plants(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            plants = db.child("farms").child(self.app.current_farm).child("plants").get()
            if plants.each():
                for plant in plants.each():
                    data = plant.val()
                    name = data.get('name', 'N/A')
                    type_ = data.get('type', 'N/A')
                    quantity = data.get('quantity', 1)
                    last_watered = data.get('last_watered', 'N/A')
                    self.tree.insert("", tk.END, values=(name, type_, quantity, last_watered))
            else:
                self.tree.insert("", tk.END, values=("No plants found", "", "", ""))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load plants: {str(e)}")

    def water_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            name = item_values[0]
            try:
                plants = db.child("farms").child(self.app.current_farm).child("plants").get()
                for plant in plants.each():
                    if plant.val().get('name') == name:
                        plant_id = plant.key()
                        break
                # ตรวจสอบสิทธิ์
                if not check_permission(self.app.current_user['localId'], self.app.current_farm, "edit_plant"):
                    messagebox.showwarning("Permission Denied", "You do not have permission to update plants.")
                    return
                # สร้างเวลาปัจจุบันในเขตเวลาประเทศไทย
                tz = pytz.timezone('Asia/Bangkok')
                current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
                # อัปเดตเวลาใน Firebase
                db.child("farms").child(self.app.current_farm).child("plants").child(plant_id).update({"last_watered": current_time})
                messagebox.showinfo("Success", "Plant watered time updated successfully!")
                self.load_plants()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update plant: {str(e)}")

    def go_to_add(self):
        if not check_permission(self.app.current_user['localId'], self.app.current_farm, "edit_plant"):
            messagebox.showwarning("Permission Denied", "You do not have permission to add plants.")
            return
        self.app.clear_window()
        from screens.add_plant_screen import AddPlantScreen
        AddPlantScreen(self.app)

    def edit_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            name = item_values[0]
            try:
                plants = db.child("farms").child(self.app.current_farm).child("plants").get()
                for plant in plants.each():
                    if plant.val().get('name') == name:
                        plant_id = plant.key()
                        break
                if not check_permission(self.app.current_user['localId'], self.app.current_farm, "edit_plant"):
                    messagebox.showwarning("Permission Denied", "You do not have permission to edit plants.")
                    return
                self.app.clear_window()
                from screens.edit_item_screen import EditItemScreen
                EditItemScreen(self.app, "plant", plant_id)
            except Exception as e:
                messagebox.showerror("Error", f"Could not find plant: {str(e)}")

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            name = item_values[0]
            try:
                plants = db.child("farms").child(self.app.current_farm).child("plants").get()
                for plant in plants.each():
                    if plant.val().get('name') == name:
                        plant_id = plant.key()
                        break
                if not check_permission(self.app.current_user['localId'], self.app.current_farm, "delete_plant"):
                    messagebox.showwarning("Permission Denied", "You do not have permission to delete plants.")
                    return
                db.child("farms").child(self.app.current_farm).child("plants").child(plant_id).remove()
                messagebox.showinfo("Success", "Plant deleted successfully!")
                self.load_plants()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete plant: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        from screens.farm_dashboard import FarmDashboardScreen
        FarmDashboardScreen(self.app)