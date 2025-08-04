import tkinter as tk

def open_dashboard(root, farm_number):
    dash_win = tk.Toplevel(root)
    dash_win.title(f"Dashboard ฟาร์ม {farm_number}")
    dash_win.geometry("400x300")

    tk.Label(dash_win, text=f"ยินดีต้อนรับสู่ Dashboard ฟาร์ม {farm_number}", font=("Tahoma", 16)).pack(pady=30)
    widget_frame = tk.Frame(dash_win)
    widget_frame.pack(pady=20)