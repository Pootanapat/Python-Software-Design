import tkinter as tk
from tkinter import ttk, messagebox

# จำลองฐานข้อมูลในหน่วยความจำ 
activity_list = []

# ฟังก์ชันบันทึกกิจกรรม
def save_data():
    activity_type = entry_type.get()
    detail = entry_detail.get()
    date = entry_date.get()

    if not activity_type or not detail or not date:
        messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
        return

    activity = {
        "type": activity_type,
        "detail": detail,
        "date": date
    }

    activity_list.append(activity)
    messagebox.showinfo("Complete", "บันทึกกิจกรรมเรียบร้อยแล้ว")
    entry_type.delete(0, tk.END)
    entry_detail.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    show_report()

# แสดงรายงาน
def show_report():
    for row in report_table.get_children():
        report_table.delete(row)

    for act in activity_list:
        report_table.insert('', tk.END, values=(act["type"], act["detail"], act["date"]))

# สร้างหน้าหลัก
root = tk.Tk()
root.title("MINIFARM")
root.geometry("800x600")
root.configure(bg="#f0f5f0")

