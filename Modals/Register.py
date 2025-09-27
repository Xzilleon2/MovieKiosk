import customtkinter as ctk

def register_modal(self):
    modal = ctk.CTkToplevel(self)
    modal.title("Register Movie")
    modal.configure(fg_color="white")
    modal.transient(self)
    modal.grab_set()

    # Modal size & center
    w, h = 400, 500
    parent_x = self.winfo_rootx()
    parent_y = self.winfo_rooty()
    parent_w = self.winfo_width()
    parent_h = self.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # ====== CARD CONTAINER ======
    card = ctk.CTkFrame(modal, fg_color="white", corner_radius=12)
    card.pack(expand=True, fill="both", padx=20, pady=20)

    # Title
    ctk.CTkLabel(
        card, text="Register Movie",
        font=("Book Antiqua", 20, "bold"),
        text_color="#665050"
    ).pack(pady=(0, 20))

    # --- Title Input ---
    ctk.CTkLabel(card, text="Title", text_color="#665050", anchor="w").pack(fill="x", padx=10)
    title_entry = ctk.CTkEntry(card, font=("Book Antiqua", 12))
    title_entry.pack(fill="x", padx=10, pady=5)

    # --- Category ---
    ctk.CTkLabel(card, text="Category", text_color="#665050", anchor="w").pack(fill="x", padx=10)
    category_combobox = ctk.CTkComboBox(card, values=["Action", "Horror", "Comedy"])
    category_combobox.pack(fill="x", padx=10, pady=5)

    # --- Price ---
    ctk.CTkLabel(card, text="Price", text_color="#665050", anchor="w").pack(fill="x", padx=10)
    price_entry = ctk.CTkEntry(card, font=("Book Antiqua", 12))
    price_entry.pack(fill="x", padx=10, pady=5)

    # --- Description ---
    ctk.CTkLabel(card, text="Description", text_color="#665050", anchor="w").pack(fill="x", padx=10)
    description_text = ctk.CTkTextbox(card, height=80)  # roughly 4 lines
    description_text.pack(fill="x", padx=10, pady=10)

    # --- Register Button ---
    register_btn = ctk.CTkButton(
        card, text="Register",
        font=("Book Antiqua", 14, "bold"),
        fg_color="#CD4126",
        hover_color="#a8321d",
        text_color="white"
    )
    register_btn.pack(pady=20, ipadx=20, ipady=10)

    return title_entry, category_combobox, price_entry, description_text, register_btn
