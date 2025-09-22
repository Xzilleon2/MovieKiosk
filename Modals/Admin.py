import tkinter as tk

def admin_login_modal(parent, controller):
    modal = tk.Toplevel(parent)
    modal.title("Admin Login")
    modal.configure(bg="#665050")
    modal.transient(parent)
    modal.grab_set()

    # Modal size
    w, h = 400, 350
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # ====== CARD CONTAINER ======
    card = tk.Frame(modal, bg="white", bd=0, relief="flat")
    card.pack(expand=True, fill="both")

    # Title
    tk.Label(
        card, text="Administrator", bg="white",
        font=("Book Antiqua", 18, "bold"), fg="#665050"
    ).pack(pady=(20, 10))

    # Username
    tk.Label(card, text="Username", bg="white", fg="#665050",
             font=("Book Antiqua", 12)).pack(anchor="w", padx=40, pady=(10, 0))
    username_entry = tk.Entry(card, font=("Book Antiqua", 12),
                              relief="solid", bd=1)
    username_entry.pack(fill="x", padx=40, pady=5, ipady=5)

    # Password
    tk.Label(card, text="Password", bg="white", fg="#665050",
             font=("Book Antiqua", 12)).pack(anchor="w", padx=40, pady=(10, 0))
    password_entry = tk.Entry(card, font=("Book Antiqua", 12),
                              relief="solid", bd=1, show="*")
    password_entry.pack(fill="x", padx=40, pady=5, ipady=5)

    # Login Button (using controller to switch pages)
    login_btn = tk.Button(
        card, text="Login",
        bg="#CD4126", fg="white",
        font=("Book Antiqua", 14, "bold"),
        relief="flat",
        activebackground="#b33620", activeforeground="white",
        command=lambda: [controller.show_frame("AdminPage"), modal.destroy()]
    )
    login_btn.pack(pady=30, ipadx=60, ipady=8)

    return username_entry, password_entry, login_btn
