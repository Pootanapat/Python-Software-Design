import tkinter as tk
from tkinter import messagebox, ttk
from firebase_config import db
from utils import check_permission
from datetime import datetime
import pytz

class AnimalScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Animals in Farm", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=10)

        # ปุ่ม Add Animal (แสดงถ้ามีสิทธิ์)
        user_id = self.app.current_user['localId']
        if check_permission(user_id, self.app.current_farm, "edit_animal"):
            add_btn = tk.Button(self.frame, text="➕ Add Animal", font=("Arial", 11, "bold"), bg="#3498db", fg="white", relief="flat", width=15, command=self.go_to_add)
            add_btn.pack(pady=5)
            add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#2980b9"))
            add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#3498db"))

        # สร้าง Treeview สำหรับแสดงตาราง
        columns = ("name", "breed", "quantity", "last_fed")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=8)
        
        # กำหนดหัวคอลัมน์
        self.tree.heading("name", text="Name")
        self.tree.heading("breed", text="Breed")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("last_fed", text="Last Fed")

        # กำหนดความกว้างของคอลัมน์
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("breed", width=150, anchor="w")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("last_fed", width=180, anchor="w")

        # ใส่ Treeview ลงในหน้าจอ
        self.tree.pack(pady=10, fill="x", padx=20)

        # ปุ่ม Feed Selected (แสดงถ้ามีสิทธิ์)
        if check_permission(user_id, self.app.current_farm, "edit_animal"):
            feed_btn = tk.Button(self.frame, text="🥛 Feed Selected", font=("Arial", 10, "bold"), bg="#f39c12", fg="white", relief="flat", width=15, command=self.feed_selected)
            feed_btn.pack(pady=5)
            feed_btn.bind("<Enter>", lambda e: feed_btn.config(bg="#d35400"))
            feed_btn.bind("<Leave>", lambda e: feed_btn.config(bg="#f39c12"))

        # ปุ่ม Edit และ Delete (แสดงถ้ามีสิทธิ์)
        if check_permission(user_id, self.app.current_farm, "edit_animal"):
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

        self.load_animals()

    def load_animals(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            animals = db.child("farms").child(self.app.current_farm).child("animals").get()
            if animals.each():
                for animal in animals.each():
                    data = animal.val()
                    name = data.get('name', 'N/A')
                    breed = data.get('breed', 'N/A')
                    quantity = data.get('quantity', 1)
                    last_fed = data.get('last_fed', 'N/A')
                    self.tree.insert("", tk.END, values=(name, breed, quantity, last_fed))
            else:
                self.tree.insert("", tk.END, values=("No animals found", "", "", ""))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load animals: {str(e)}")

    def feed_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            name = item_values[0]
            try:
                animals = db.child("farms").child(self.app.current_farm).child("animals").get()
                for animal in animals.each():
                    if animal.val().get('name') == name:
                        animal_id = animal.key()
                        break
                # ตรวจสอบสิทธิ์
                if not check_permission(self.app.current_user['localId'], self.app.current_farm, "edit_animal"):
                    messagebox.showwarning("Permission Denied", "You do not have permission to update animals.")
                    return
                # สร้างเวลาปัจจุบันในเขตเวลาประเทศไทย
                tz = pytz.timezone('Asia/Bangkok')
                current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
                # อัปเดตเวลาใน Firebase
                db.child("farms").child(self.app.current_farm).child("animals").child(animal_id).update({"last_fed": current_time})
                messagebox.showinfo("Success", "Animal fed time updated successfully!")
                self.load_animals()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update animal: {str(e)}")

    def go_to_add(self):
        if not check_permission(self.app.current_user['localId'], self.app.current_farm, "edit_animal"):
            messagebox.showwarning("Permission Denied", "You do not have permission to add animals.")
            return
        self.app.clear_window()
        from screens.add_animal_screen import AddAnimalScreen
        AddAnimalScreen(self.app)

    def edit_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            name = item_values[0]
            try:
                animals = db.child("farms").child(self.app.current_farm).child("animals").get()
                for animal in animals.each():
                    if animal.val().get('name') == name:
                        animal_id = animal.key()
                        break
                if not check_permission(self.app.current_user['localId'], self.app.current_farm, "edit_animal"):
                    messagebox.showwarning("Permission Denied", "You do not have permission to edit animals.")
                    return
                self.app.clear_window()
                from screens.edit_item_screen import EditItemScreen
                EditItemScreen(self.app, "animal", animal_id)
            except Exception as e:
                messagebox.showerror("Error", f"Could not find animal: {str(e)}")

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            name = item_values[0]
            try:
                animals = db.child("farms").child(self.app.current_farm).child("animals").get()
                for animal in animals.each():
                    if animal.val().get('name') == name:
                        animal_id = animal.key()
                        break
                if not check_permission(self.app.current_user['localId'], self.app.current_farm, "delete_animal"):
                    messagebox.showwarning("Permission Denied", "You do not have permission to delete animals.")
                    return
                db.child("farms").child(self.app.current_farm).child("animals").child(animal_id).remove()
                messagebox.showinfo("Success", "Animal deleted successfully!")
                self.load_animals()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete animal: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        from screens.farm_dashboard import FarmDashboardScreen
        FarmDashboardScreen(self.app)