import tkinter as tk
from tkinter import ttk

class TableWithFilters:
    def __init__(self, parent, columns, data, page_size=50):
        self.parent = parent
        self.columns = columns
        self.page_size = page_size

        self.all_data = data.copy()
        self.filtered_data = data.copy()
        self.offset = 0

        # ---------- Main frame ----------
        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # ---------- Horizontal scrollable filter frame ----------
        filter_container = tk.Frame(self.main_frame)
        filter_container.grid(row=0, column=0, sticky="ew")

        self.filter_canvas = tk.Canvas(filter_container, height=30)
        self.filter_canvas.pack(side="top", fill="x", expand=True)

        self.filter_scroll = tk.Scrollbar(filter_container, orient="horizontal",
                                          command=self.filter_canvas.xview)
        self.filter_scroll.pack(side="bottom", fill="x")
        self.filter_canvas.configure(xscrollcommand=self.filter_scroll.set)

        self.filter_frame = tk.Frame(self.filter_canvas)
        self.filter_canvas.create_window((0,0), window=self.filter_frame, anchor="nw")
        self.filter_frame.bind("<Configure>", lambda e: self.filter_canvas.configure(
            scrollregion=self.filter_canvas.bbox("all")
        ))

        self.filter_vars = {}
        self.filter_entries = {}

        for col in columns:
            frm = tk.Frame(self.filter_frame)
            frm.pack(side="left", padx=1, pady=2)

            var = tk.StringVar()
            entry = tk.Entry(frm, textvariable=var)
            entry.pack(side="left", fill="x", expand=True)
            entry.insert(0, "🔍")
            entry.bind("<FocusIn>", lambda e, v=var: self._clear_placeholder(v))
            entry.bind("<FocusOut>", lambda e, v=var: self._add_placeholder(v))
            var.trace_add("write", lambda *_ , c=col: self._apply_filters())

            btn = tk.Button(frm, text="▾", width=2,
                            command=lambda c=col: self._show_unique_checkbox(c))
            btn.pack(side="left")

            self.filter_vars[col] = var
            self.filter_entries[col] = entry

        # ---------- Treeview ----------
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        self.tree.grid(row=1, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_column(c))
            self.tree.column(col, width=140, stretch=True)

        # Adjust filter entries width when Treeview column resizes
        self.tree.bind("<Configure>", self._adjust_filter_widths)

        self._load_page()

    # ---------- Adjust filter entry widths ----------
    def _adjust_filter_widths(self, event=None):
        for col in self.columns:
            try:
                width = self.tree.column(col, width=None)
                self.filter_entries[col].config(width=max(int(width/7),5))  # approx char width
            except Exception:
                pass

    # ---------- Placeholder helpers ----------
    def _clear_placeholder(self, var):
        if var.get() == "🔍":
            var.set("")

    def _add_placeholder(self, var):
        if not var.get():
            var.set("🔍")

    # ---------- Filter logic ----------
    def _apply_filters(self):
        self.filtered_data = self.all_data.copy()
        for col, var in self.filter_vars.items():
            val = var.get()
            if val and val != "🔍":
                idx = self.columns.index(col)
                self.filtered_data = [r for r in self.filtered_data if val.lower() in str(r[idx]).lower()]
        self.offset = 0
        self._load_page()

    # ---------- Unique values popup with search + scroll + select/unselect all ----------
    def _show_unique_checkbox(self, col):
        idx = self.columns.index(col)
        unique_vals = sorted({str(r[idx]) for r in self.all_data})

        popup = tk.Toplevel(self.parent)
        popup.title(f"Filter {col}")
        popup.geometry("350x400")
        popup.transient(self.parent)

        popup.grid_rowconfigure(2, weight=1)
        popup.grid_columnconfigure(0, weight=1)

        # ---------- Search Entry ----------
        search_var = tk.StringVar()
        search_entry = tk.Entry(popup, textvariable=search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(popup)
        btn_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        tk.Button(btn_frame, text="Select All", command=lambda: self._check_all(vars_dict, True)).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="Unselect All", command=lambda: self._check_all(vars_dict, False)).pack(side="left", expand=True, fill="x", padx=2)

        # ---------- Scrollable checkbox frame ----------
        container = tk.Frame(popup)
        container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(container)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        checkbox_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        canvas_window = canvas.create_window((0,0), window=checkbox_frame, anchor="nw")
        checkbox_frame.bind("<Configure>", on_frame_configure)

        # ---------- Add checkboxes ----------
        vars_dict = {}
        widgets_dict = {}
        for val in unique_vals:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(checkbox_frame, text=val, variable=var, anchor="w")
            chk.pack(fill="x", anchor="w")
            vars_dict[val] = var
            widgets_dict[val] = chk

        # ---------- Search functionality ----------
        def update_checkboxes(*_):
            s = search_var.get().lower()
            for val, chk in widgets_dict.items():
                if s in val.lower():
                    chk.pack(fill="x", anchor="w")
                else:
                    chk.pack_forget()
        search_var.trace_add("write", update_checkboxes)

        # ---------- Apply ----------
        tk.Button(popup, text="Apply", command=lambda: self._apply_checkbox_filter(idx, vars_dict, popup)).grid(row=3, column=0, sticky="ew", padx=5, pady=5)

    # Helper function for select/unselect all
    def _check_all(self, vars_dict, value):
        for var in vars_dict.values():
            var.set(value)

    def _apply_checkbox_filter(self, idx, vars_dict, popup):
        selected = [val for val, var in vars_dict.items() if var.get()]
        self.filtered_data = [r for r in self.all_data if str(r[idx]) in selected]
        self.offset = 0
        self._load_page()
        popup.destroy()

    # ---------- Sorting ----------
    def _sort_column(self, col):
        idx = self.columns.index(col)
        self.filtered_data.sort(key=lambda r: str(r[idx]))
        self._load_page()

    # ---------- Pagination ----------
    def _load_page(self):
        self.tree.delete(*self.tree.get_children())
        page = self.filtered_data[self.offset:self.offset+self.page_size]
        for row in page:
            self.tree.insert("", "end", values=row)

    def load_data(self, new_data):
        self.all_data = new_data.copy()
        self.filtered_data = new_data.copy()
        self.offset = 0
        self._load_page()
