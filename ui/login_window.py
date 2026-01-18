import tkinter as tk
from tkinter import messagebox, ttk
from db.db_factory import connect
from ui.main_window import open_main_window

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamza's Database Login")
        self.root.resizable(False, False)

        # ---------- Labels ----------
        labels = [
            "Database Type",
            "Host / IP",
            "Port",
            "Username",
            "Password"
        ]
        for i, text in enumerate(labels):
            tk.Label(root, text=text).grid(
                row=i, column=0, padx=10, pady=6, sticky="w"
            )

        # ---------- Inputs ----------
        self.db_type = ttk.Combobox(
            root,
            values=["MySQL", "PostgreSQL", "MSSQL"],
            state="readonly",
            width=20
        )
        self.db_type.current(0)

        self.host_entry = tk.Entry(root, width=23)
        self.port_entry = tk.Entry(root, width=23)
        self.user_entry = tk.Entry(root, width=23)
        self.pass_entry = tk.Entry(root, width=23, show="*")

        self.host_entry.insert(0, "localhost")
        self.port_entry.insert(0, "3306")

        self.db_type.grid(row=0, column=1, padx=10, pady=6)
        self.host_entry.grid(row=1, column=1, padx=10, pady=6)
        self.port_entry.grid(row=2, column=1, padx=10, pady=6)
        self.user_entry.grid(row=3, column=1, padx=10, pady=6)
        self.pass_entry.grid(row=4, column=1, padx=10, pady=6)

        # ---------- Events ----------
        self.db_type.bind("<<ComboboxSelected>>", self._update_port)

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())

        # ---------- Button ----------
        tk.Button(
            root,
            text="Connect",
            width=20,
            command=self.login
        ).grid(row=5, column=1, pady=14)

    # --------------------------------------------------
    # Auto-update default port based on DB type
    # --------------------------------------------------
    def _update_port(self, event=None):
        default_ports = {
            "MySQL": "3306",
            "PostgreSQL": "5432",
            "MSSQL": "1433"
        }
        self.port_entry.delete(0, tk.END)
        self.port_entry.insert(0, default_ports[self.db_type.get()])

    # --------------------------------------------------
    # Login Logic (with port handling and Enter key)
    # --------------------------------------------------
    def login(self):
        try:
            host = self.host_entry.get().strip()
            port = int(self.port_entry.get().strip())  # <-- Always int
            user = self.user_entry.get().strip()
            password = self.pass_entry.get()
            db_type = self.db_type.get()

            if not host or not port or not user:
                raise ValueError("Host, Port, and Username are required")

            # Connect to DB
            conn = connect(
                db_type=db_type,
                host=host,
                port=port,
                user=user,
                password=password
            )

            self.root.destroy()
            open_main_window(conn)

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

