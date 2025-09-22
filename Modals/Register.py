import tkinter as tk
import tkinter.ttk as ttk
import os as os

# ========================= MODAL FUNCTION ============================
def register_modal(self):
    modal = tk.Toplevel(self)
    modal.title("Register Movie")
    modal.configure(bg="white")
    modal.transient(self)
    modal.grab_set()

    # Modal size
    w, h = 400, 500

    # Get parent window position and size
    parent_x = self.winfo_rootx()
    parent_y = self.winfo_rooty()
    parent_w = self.winfo_width()
    parent_h = self.winfo_height()

    # Center coordinates
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2)

    # Apply geometry
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # Title
    tk.Label(modal, text="Register Movie", font=("Book Antiqua", 20, "bold"),
             fg="#665050", bg="white").pack(pady=20)

    # Inputs
    tk.Label(modal, text="Title", bg="white", fg="#665050").pack(anchor="w", padx=20)
    tk.Entry(modal).pack(fill="x", padx=20, pady=5)

    tk.Label(modal, text="Category", bg="white", fg="#665050").pack(anchor="w", padx=20)
    ttk.Combobox(modal, values=["Action", "Horror", "Comedy"], state="readonly").pack(fill="x", padx=20, pady=5)

    tk.Label(modal, text="Price", bg="white", fg="#665050").pack(anchor="w", padx=20)
    tk.Entry(modal).pack(fill="x", padx=20, pady=5)

    tk.Label(modal, text="Description", bg="white", fg="#665050").pack(anchor="w", padx=20)
    tk.Text(modal, height=4).pack(fill="x", padx=20, pady=10)

    # Register button inside modal
    tk.Button(modal, text="Register", bg="#CD4126", fg="white",
              font=("Book Antiqua", 14), relief="flat").pack(pady=20, ipadx=20, ipady=10)