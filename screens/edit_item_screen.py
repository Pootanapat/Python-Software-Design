import tkinter as tk
from tkinter import messagebox
from firebase_config import db
from utils import add_log

class EditItemScreen:
    def __init__(self, app, item_type, item_id):
        self.app = app
        self.item_type = item_type  # "animal" or "plant"
        self.item_id = item_id
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title = "Edit Animal" if self.item_type == "animal" else "Edit Plant"
        title_label = tk.Label(self.frame, text=title, font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=10)

        # ช่องกรอกข้อมูล
        tk.Label(self.frame, text="Name", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.name_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.name_entry.pack(pady=5)

        if self.item_type == "animal":
            tk.Label(self.frame, text="Breed", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
            self.breed_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
            self.breed_entry.pack(pady=5)
        else:
            tk.Label(self.frame, text="Type", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
            self.type_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
            self.type_entry.pack(pady=5)

        tk.Label(self.frame, text="Quantity", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.quantity_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.quantity_entry.pack(pady=5)

        if self.item_type == "animal":
            tk.Label(self.frame, text="Last Fed (YYYY-MM-DD)", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
            self.last_fed_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
            self.last_fed_entry.pack(pady=5)
        else:
            tk.Label(self.frame, text="Last Watered (YYYY-MM-DD)", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
            self.last_watered_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
            self.last_watered_entry.pack(pady=5)

        # ปุ่ม Update
        update_btn = tk.Button(self.frame, text="✅ Update", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", relief="flat", width=15, command=self.update_item)
        update_btn.pack(pady=10)
        update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#27ae60"))
        update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#2ecc71"))

        # ปุ่ม Delete
        delete_btn = tk.Button(self.frame, text="🗑️ Delete", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", width=10, command=self.delete_item)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#c0392b"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#e74c3c"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

        self.load_item()

    def load_item(self):
        try:
            item = db.child("farms").child(self.app.current_farm).child(f"{self.item_type}s").child(self.item_id).get()
            data = item.val()
            self.name_entry.insert(0, data.get("name", ""))
            if self.item_type == "animal":
                self.breed_entry.insert(0, data.get("breed", ""))
                self.last_fed_entry.insert(0, data.get("last_fed", ""))
            else:
                self.type_entry.insert(0, data.get("type", ""))
                self.last_watered_entry.insert(0, data.get("last_watered", ""))
            self.quantity_entry.insert(0, str(data.get("quantity", 1)))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load item: {str(e)}")

    def update_item(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        if not name or not quantity:
            messagebox.showwarning("Warning", "Please fill in all required fields.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        try:
            if self.item_type == "animal":
                breed = self.breed_entry.get()
                last_fed = self.last_fed_entry.get()
                data = {
                    "name": name,
                    "breed": breed,
                    "quantity": quantity,
                    "last_fed": last_fed or "Not Set",
                    "added_by": self.app.current_user['localId']
                }
            else:
                type_ = self.type_entry.get()
                last_watered = self.last_watered_entry.get()
                data = {
                    "name": name,
                    "type": type_,
                    "quantity": quantity,
                    "last_watered": last_watered or "Not Set",
                    "added_by": self.app.current_user['localId']
                }

            db.child("farms").child(self.app.current_farm).child(f"{self.item_type}s").child(self.item_id).set(data)
            add_log(self.app.current_farm, self.app.current_user['localId'], f"updated_{self.item_type}", data)
            messagebox.showinfo("Success", f"{self.item_type.capitalize()} updated successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update item: {str(e)}")

    def delete_item(self):
        try:
            db.child("farms").child(self.app.current_farm).child(f"{self.item_type}s").child(self.item_id).remove()
            add_log(self.app.current_farm, self.app.current_user['localId'], f"deleted_{self.item_type}", {})
            messagebox.showinfo("Success", f"{self.item_type.capitalize()} deleted successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete item: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        if self.item_type == "animal":
            from screens.animal_screen import AnimalScreen
            AnimalScreen(self.app)
        else:
            from screens.plant_screen import PlantScreen
            PlantScreen(self.app)