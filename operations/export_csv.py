import csv
from tkinter.filedialog import asksaveasfilename

def export_csv(columns, rows):
    file = asksaveasfilename(defaultextension=".csv")
    if not file:
        return

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
