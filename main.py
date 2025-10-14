import tkinter as tk
from screens.login_screen import LoginScreen

class FarmApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MINIFARM")
        self.root.geometry("600x400")
        self.current_user = None
        self.current_farm = None

        # Start with login screen
        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginScreen(self)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FarmApp()
    app.run()