import tkinter as tk
from tkinter import messagebox
from utils import check_permission

class ManagerScreen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg="#f5f5f5")
        self.frame.pack(fill="both", expand=True)

        # หัวเรื่อง
        title_label = tk.Label(self.frame, text="Farm Manager", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#2c3e50")
        title_label.pack(pady=20)

        # ปุ่ม Invite Member
        invite_btn = tk.Button(self.frame, text="📧 Invite Member", font=("Arial", 12, "bold"), bg="#3498db", fg="white", relief="flat", width=20, command=self.go_to_invite)
        invite_btn.pack(pady=10)
        invite_btn.bind("<Enter>", lambda e: invite_btn.config(bg="#2980b9"))
        invite_btn.bind("<Leave>", lambda e: invite_btn.config(bg="#3498db"))

        # ปุ่ม Manage Members
        manage_btn = tk.Button(self.frame, text="👥 Manage Members", font=("Arial", 12, "bold"), bg="#9b59b6", fg="white", relief="flat", width=20, command=self.show_members)
        manage_btn.pack(pady=10)
        manage_btn.bind("<Enter>", lambda e: manage_btn.config(bg="#8e44ad"))
        manage_btn.bind("<Leave>", lambda e: manage_btn.config(bg="#9b59b6"))

        # ปุ่ม View Logs (ถ้ามี)
        logs_btn = tk.Button(self.frame, text="📋 View Logs", font=("Arial", 12, "bold"), bg="#f39c12", fg="white", relief="flat", width=20, command=self.show_logs)
        logs_btn.pack(pady=10)
        logs_btn.bind("<Enter>", lambda e: logs_btn.config(bg="#d35400"))
        logs_btn.bind("<Leave>", lambda e: logs_btn.config(bg="#f39c12"))

        # ปุ่ม Back
        back_btn = tk.Button(self.frame, text="← Back", font=("Arial", 10, "bold"), bg="#95a5a6", fg="white", relief="flat", width=10, command=self.go_back)
        back_btn.pack(pady=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#7f8c8d"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#95a5a6"))

    def go_to_invite(self):
        self.app.clear_window()
        from screens.invite_member_screen import InviteMemberScreen
        InviteMemberScreen(self.app)

    def show_members(self):
        self.app.clear_window()
        from screens.role_permission_screen import RolePermissionScreen
        RolePermissionScreen(self.app)

    def show_logs(self):
        # ถ้าคุณมีหน้าแสดง log แล้ว ให้เรียกใช้ที่นี่
        messagebox.showinfo("Coming Soon", "Logs feature will be added soon.")

    def go_back(self):
        self.app.clear_window()
        from screens.farm_dashboard import FarmDashboardScreen
        FarmDashboardScreen(self.app)