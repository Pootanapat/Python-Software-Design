import tkinter as tk
from tkinter import ttk, messagebox

#จำลอง
activity_list = []

#บันทึก
def save_data():
    activity_type  = entry_type.get()
    detail = entry_detail.get()
    date = entry_date.get()

    if not activity_type or not detail or not date:
        messagebox.showerror("Error", "กรุฯษใส่ชื่อให้ครบถ้วน")
        return

    activity ={
        "type": activity_type,
        "detail": detail,
        "date": date
    } 

    activity_list.append(activity)
    messagebox.showinfo("Success", "บันทึกกิจกรรมเรียบร้อยแล้ว")
    entry_type.delete(0, tk.END)
    entry_detail.delete(0, tk.END)
    show_report()

#แสดงรายงาน
def show_report():
    for row in report_table.get_children():
        report_table.delete(row)

    for act in activity_list:
        report_table.insert('', tk.END, values=(act["type"], act["detail"], act["date"]))

#สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Mini Farm")
root.geometry("800x600")
root.configure(bg="#f0f5f0")

font_title = ("Kanit", 16, "bold")
font_label = ("Kanit", 12)
font_entry = ("Kanit", 12)

#ส่วนหัว
tk.Label(root, text="บันทึกกิจกรรม", font=font_title, bg="#f0f5f0").pack(pady=10)

#กรอกข้อมูล
form_frame = tk.Frame(root, bg="#e8f5e9", padx=15, pady=15)
form_frame.pack(pady=5, fill="x")

tk.Label(form_frame, text="พืช:", font=font_label, bg="#e8f5e9").grid(row=0, column=0, sticky="e")
entry_type = tk.Entry(form_frame, font=font_entry, width=40)
entry_type.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="รายละเอียด:", font=font_label, bg="#e8f5e9").grid(row=1, column=0, sticky="e")
entry_detail = tk.Entry(form_frame, font=font_entry, width=40)
entry_detail.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="วันที่ (YYYY-MM-DD):", font=font_label, bg="#e8f5e9").grid(row=2, column=0, sticky="e")
entry_date = tk.Entry(form_frame, font=font_entry, width=40)
entry_date.grid(row=2, column=1, padx=10, pady=5)

#ปุ่มบันทึก
tk.Button(form_frame, text="บันทึก", command=save_data, font=font_label, bg="#81c784", fg="white").grid(row=3, columnspan=2, pady=10)

#ตารางรายงาน
tk.Label(root, text="รายงานกิจกรรม", font=font_title, bg="#f0f5f0").pack

#สไลล์ตาราง
style = ttk.Style()
style.configure("Treeview.Heading", font=font_entry, rowheight=30)


