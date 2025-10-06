import customtkinter as ctk
from tkinter import messagebox

def choice_modal(parent, cash_callback=None, online_callback=None, ticket=None):
    modal = ctk.CTkToplevel(parent)
    modal.title("Select Payment Method")
    modal.configure(fg_color="#E8FFD7")  # Light green background
    modal.transient(parent)
    modal.grab_set()

    # Modal size & center
    w, h = 400, 300
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")
    modal.update()
    modal.attributes('-topmost', True)

    # ====== CARD CONTAINER ======
    card = ctk.CTkFrame(modal, fg_color="#93DA97", corner_radius=15)
    card.pack(expand=True, fill="both", padx=20, pady=20)

    # Title
    ctk.CTkLabel(
        card,
        text="Choose Payment",
        font=("Book Antiqua", 20, "bold"),
        text_color="#3E5F44"
    ).pack(pady=(60, 20))

    # Buttons container
    btn_frame = ctk.CTkFrame(card, fg_color="#93DA97")
    btn_frame.pack(expand=True, fill="both", padx=20, pady=(10, 20))
    btn_frame.columnconfigure((0, 1), weight=1, uniform="btns")

    # Cash Button
    def on_cash():
        print(f"[DEBUG] Cash button clicked. Ticket data: {ticket}")
        if cash_callback:
            cash_callback(ticket)
        modal.destroy()

    cash_btn = ctk.CTkButton(
        btn_frame,
        text="💵 Cash",
        font=("Book Antiqua", 16, "bold"),
        fg_color="#22c55e",
        hover_color="#16a34a",
        text_color="#E8FFD7",
        corner_radius=12,
        height=60,
        command=on_cash
    )
    cash_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Online Button
    online_btn = ctk.CTkButton(
        btn_frame,
        text="💳 Online",
        font=("Book Antiqua", 16, "bold"),
        fg_color="#3E5F44",
        hover_color="#5E936C",
        text_color="#E8FFD7",
        corner_radius=12,
        height=60,
        command=lambda: messagebox.showinfo(
            "Underdevelopment",
            "This feature is currently under development.\nSorry for the inconvenience!",
            parent=modal
        )
    )
    online_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    return cash_btn, online_btn
