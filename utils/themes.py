from tkinter import ttk

def apply_dark_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".",
        background="#2b2b2b",
        foreground="#ffffff",
        fieldbackground="#3c3f41"
    )

    style.configure("Treeview",
        background="#3c3f41",
        foreground="#ffffff",
        rowheight=24,
        fieldbackground="#3c3f41"
    )

    style.map("Treeview",
        background=[("selected", "#007acc")]
    )

    root.configure(bg="#2b2b2b")
