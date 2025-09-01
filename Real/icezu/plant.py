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

#ลบกิจกรรม
def delete_activity():
    selected_item = report_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "กรุณาเลือกกิจกรรมที่ต้องการลบ")
        return

    for item in selected_item:
        report_table.delete(item)
        activity_list.remove(activity_list[int(item)])  # ลบจากฐานข้อมูลจำลอง

    messagebox.showinfo("Complete", "ลบกิจกรรมเรียบร้อยแล้ว")
    show_report()

#แสดงรายงาน
def show_report():
    for row in report_table.get_children():
        report_table.delete(row)

    for act in activity_list:
        report_table.insert('', tk.END, values=(act["type"], act["detail"], act["date"]))

    # สรุปข้อมูล (รวมจำนวนพืช)
def show_summary():
    if not activity_list:
        messagebox.showinfo("Summary", "ไม่มีข้อมูลกิจกรรม")
        return

    summary = {}
    for act in activity_list:
        plant_type = act["type"]
        try:
            quantity = int(act["detail"])
        except ValueError:
            quantity = 0
        summary[plant_type] = summary.get(plant_type, 0) + quantity

    summary_text = "สรุปจำนวนสัตว์:\n"
    for animal_type, total in summary.items():
        summary_text += f"{plant_type}: {total} กิโลกรัม\n"

    messagebox.showinfo("Summary", summary_text)



            
# สร้างหน้าหลัก
root = tk.Tk()
root.title("MINIFARM")
root.geometry("800x600")
root.configure(bg="#f0f5f0")

font_title = ("Kanit", 16, "bold")
font_label = ("Kanit", 12)
font_entry = ("Kanit", 11)

# ส่วนหัว
tk.Label(root, text="ฟาร์ม", font=font_title, bg="#f0f5f0").pack(pady=10)



# ฟอร์ม
form_frame = tk.Frame(root, bg="#e8f5e9", padx=15, pady=15)
form_frame.pack(pady=5, fill="x")

tk.Label(form_frame, text="ชนิดพืช:", font=font_label, bg="#e8f5e9").grid(row=0, column=0, sticky="e")
entry_type = tk.Entry(form_frame, font=font_entry, width=40)
entry_type.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="จำนวน:", font=font_label, bg="#e8f5e9").grid(row=1, column=0, sticky="e")
entry_detail = tk.Entry(form_frame, font=font_entry, width=40)
entry_detail.grid(row=1, column=1, padx=10, pady=5)


tk.Label(form_frame, text="วันที่ (YYYY-MM-DD):", font=font_label, bg="#e8f5e9").grid(row=2, column=0, sticky="e")
entry_date = tk.Entry(form_frame, font=font_entry, width=40)
entry_date.grid(row=2, column=1, padx=10, pady=5)

# สร้าง frame สำหรับปุ่มจัดเรียงแนวนอน
button_frame = tk.Frame(root, bg="#f0f5f0")
button_frame.pack(pady=10)

# ปุ่มบันทึก
btn_save = tk.Button(button_frame, text="บันทึกการจัดเก็บ", font=font_label, bg="#66bb6a", fg="white", command=save_data)
btn_save.pack(side="left", padx=10)

# ปุ่มลบกิจกรรม
btn_delete = tk.Button(button_frame, text="ลบการจัดเก็บ", font=font_label, bg="#ef5350", fg="white", command=delete_activity)
btn_delete.pack(side="left", padx=10)

# ปุ่มสรุปข้อมูล
btn_summary = tk.Button(button_frame, text="สรุปข้อมูล", font=font_label, bg="#42a5f5", fg="white", command=show_summary)
btn_summary.pack(side="left", padx=10)


# รายงาน
tk.Label(root, text=" รายงานการจัดเก็บพืช", font=font_title, bg="#f0f5f0").pack()

report_table = ttk.Treeview(root, columns=("ประเภท", "จำนวน", "วันที่"), show="headings")
report_table.heading("ประเภท", text="ประเภท")
report_table.heading("จำนวน", text="จำนวน")
report_table.heading("วันที่", text="วันที่")
report_table.pack(padx=15, pady=10, fill="both", expand=True)

# สไลeตาราง
style = ttk.Style()
style.configure("Treeview.Heading", font=("Kanit", 11, "bold"))
style.configure("Treeview", font=("Kanit", 10), rowheight=28)

# แสดงข้อมูล
show_report()

root.mainloop()
