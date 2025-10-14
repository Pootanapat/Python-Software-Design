import tkinter as tk
from tkinter import messagebox
from firebase_config import db
from utils import add_log
from datetime import datetime
import pytz

class AddAnimalScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Add New Animal", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=10)

        # ช่องกรอกข้อมูล
        tk.Label(self.frame, text="Name", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.name_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.name_entry.pack(pady=5)

        tk.Label(self.frame, text="Breed", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.breed_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.breed_entry.pack(pady=5)

        tk.Label(self.frame, text="Quantity", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.quantity_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.quantity_entry.pack(pady=5)

        tk.Label(self.frame, text="Last Fed (YYYY-MM-DD)", font=("Arial", 11), bg="#f5f5f5", fg="#2c3e50").pack(pady=(5, 2))
        self.last_fed_entry = tk.Entry(self.frame, font=("Arial", 11), width=30, relief="solid", bd=1)
        self.last_fed_entry.pack(pady=5)

        # ปุ่ม Add
        add_btn = tk.Button(self.frame, text="✅ Add Animal", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", relief="flat", width=20, command=self.add_animal)
        add_btn.pack(pady=20)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#27ae60"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#2ecc71"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

    def add_animal(self):
        name = self.name_entry.get()
        breed = self.breed_entry.get()
        quantity = self.quantity_entry.get()
        last_fed = self.last_fed_entry.get()

        if not name or not breed or not quantity:
            messagebox.showwarning("Warning", "Please fill in all required fields.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        user_id = self.app.current_user['localId']
        try:
            animal_data = {
                "name": name,
                "breed": breed,
                "quantity": quantity,
                "last_fed": last_fed or "Not Set",
                "added_by": user_id
            }
            animal_id = db.child("farms").child(self.app.current_farm).child("animals").push(animal_data)["name"]
            add_log(self.app.current_farm, user_id, "added_animal", animal_data)
            messagebox.showinfo("Success", "Animal added successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add animal: {str(e)}")

    def go_back(self):
        self.app.clear_window()
        from screens.animal_screen import AnimalScreen
        AnimalScreen(self.app)