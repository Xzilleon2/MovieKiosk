# ui_styles.py
import tkinter as tk
from tkinter import ttk

def setup_table_style():
    style = ttk.Style()
    style.theme_use("default")

    # Remove borders
    style.layout("Custom.Treeview", [
        ("Treeview.treearea", {"sticky": "nswe"})
    ])

    # Table look
    style.configure("Custom.Treeview",
                    background="#FFFFFF",
                    fieldbackground="#FFFFFF",
                    foreground="#665050",
                    font=("Book Antiqua", 12),
                    rowheight=40)

    # Header look
    style.configure("Custom.Treeview.Heading",
                    font=("Book Antiqua", 18, "bold"),
                    background="#EFE9E0",
                    foreground="#665050",
                    relief="flat",
                    padding=10)

    # Selection + hover
    style.map("Custom.Treeview",
              background=[
                  ("selected", "#D4A373"),
                  ("active", "#EFE9E0")
              ],
              foreground=[
                  ("selected", "white"),
                  ("active", "#665050")
              ])


def zebra_striping(table):
    """Apply alternating row colors (odd/even) to the Treeview."""
    table.tag_configure('oddrow', background="#F9F9F9")
    table.tag_configure('evenrow', background="#FFFFFF")

    for index, item in enumerate(table.get_children()):
        tag = "oddrow" if index % 2 else "evenrow"
        table.item(item, tags=(tag,))


def sort_table(table, col, reverse=False):
    """Sort the Treeview by column."""
    data = [(table.set(k, col), k) for k in table.get_children('')]
    data.sort(reverse=reverse)

    for index, (val, k) in enumerate(data):
        table.move(k, '', index)

    # Toggle sort order next click
    table.heading(col, command=lambda: sort_table(table, col, not reverse))


def disable_resize(event, table):
    """Prevent resizing columns by dragging separator."""
    if table.identify_region(event.x, event.y) == "separator":
        return "break"