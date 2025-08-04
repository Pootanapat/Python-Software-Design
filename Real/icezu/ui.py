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

#แสดงรายงาน
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

font_title = ("Kanit", 16, "bold")
font_label = ("Kanit", 12)
font_entry = ("Kanit", 11)

# ส่วนหัว
tk.Label(root, text="บันทึกกิจกรรมฟาร์ม", font=font_title, bg="#f0f5f0").pack(pady=10)

# ฟอร์ม
form_frame = tk.Frame(root, bg="#e8f5e9", padx=15, pady=15)
form_frame.pack(pady=5, fill="x")

tk.Label(form_frame, text="ชนิดพืช:", font=font_label, bg="#e8f5e9").grid(row=0, column=0, sticky="e")
entry_type = tk.Entry(form_frame, font=font_entry, width=40)
entry_type.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="รายละเอียด:", font=font_label, bg="#e8f5e9").grid(row=1, column=0, sticky="e")
entry_detail = tk.Entry(form_frame, font=font_entry, width=40)
entry_detail.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="วันที่ (YYYY-MM-DD):", font=font_label, bg="#e8f5e9").grid(row=2, column=0, sticky="e")
entry_date = tk.Entry(form_frame, font=font_entry, width=40)
entry_date.grid(row=2, column=1, padx=10, pady=5)

# บันทึก
tk.Button(root, text="บันทึกกิจกรรม", font=font_label, bg="#66bb6a", fg="white", command=save_data)\
    .pack(pady=10)

# รายงาน
tk.Label(root, text="📋 รายงานกิจกรรม", font=font_title, bg="#f0f5f0").pack()

report_table = ttk.Treeview(root, columns=("ประเภท", "รายละเอียด", "วันที่"), show="headings")
report_table.heading("ประเภท", text="ประเภท")
report_table.heading("รายละเอียด", text="รายละเอียด")
report_table.heading("วันที่", text="วันที่")
report_table.pack(padx=15, pady=10, fill="both", expand=True)

# สไลeตาราง
style = ttk.Style()
style.configure("Treeview.Heading", font=("Kanit", 11, "bold"))
style.configure("Treeview", font=("Kanit", 10), rowheight=28)

# แสดงข้อมูล
show_report()

root.mainloop()




