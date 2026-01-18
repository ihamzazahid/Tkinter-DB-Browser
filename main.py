import tkinter as tk
from ui.login_window import LoginWindow
from utils.themes import apply_dark_theme

if __name__ == "__main__":
    root = tk.Tk()
    apply_dark_theme(root)
    LoginWindow(root)
    root.mainloop()
